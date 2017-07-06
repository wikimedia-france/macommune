window.macommune = {};

macommune.Autocomplete = function( id, parentId ) {
    this.id = id;
    this.parentId = parentId;
    var cache = {};
    
    this.init = function() {
        $( this.id ).autocomplete( {
	        source: this.getData,
            select: this.onSelect,
            appendTo: this.parentId,
        } );
    };
    
    this.getData = function( request, response ) {
        var term = request.term;
        if ( term in cache ) {
            response( cache[ term ] );
            return;
        }
        $.get( '/api/complete/' + term ).then( function( data ) {
            cache[ term ] = data.values;
            response( data.values );
        } );
    };
    
    this.onSelect = function( event, ui ) {
        navigation.loadPage( ui.item.qid, ui.item.value, true );
    };
    
    return this.init();
}


macommune.Navigation = function() {
    this.qid = null;
    this.title = null;
    this.ui = undefined;
    
    var nav = this;

    this.init = function() {
        var params = nav.getParams();
        
        if ( nav.ui === undefined ) {
            nav.ui = new macommune.Ui( params[ 0 ] );
        }
        
        if ( params[ 0 ] === undefined || params[ 0 ] === '' ) {
            if ( nav.qid !== null ) {
                nav.resetView();
            }
            return;
        }
        nav.loadPage( params[ 0 ], params[ 1 ] );
    };
    
    this.loadPage = function( qid, title, changeHistory ) {
        nav.qid = qid;
        nav.title = title
        
        nav.ui.changePage( nav.qid, nav.fetchData() );
        
        if ( changeHistory === true ) {
            history.pushState( { qid: nav.qid, title: nav.title }, '', '/' + nav.qid + '/' + nav.title );
        }
    }

    this.resetView = function() {
        nav.qid = null;
        nav.title = null;
        nav.ui.setHome();
    };

    this.fetchData = function() {
        return $.get( '/api/item/' + nav.qid )
    };

    this.getParams = function() {
        var params = window.location.pathname.split( '/' );
        params.shift();
        return params
    };
    
    this.onpopstate = function( event ) {
        if ( event.state === null ) {
            nav.init()
            return;
        }
        navigation.loadPage( event.state.qid, event.state.title );
    };
    
    return this.init();
}

macommune.Ui = function( qid ) {
    this.qid = qid;
    this.data = null;
    this.homeVue;
    this.spinnerVue;
    
    var ui = this;
    
    this.init = function() {
        console.log( 'new UI initialised' )
        if ( ui.qid === undefined ) {
            ui.setHome();
        }
        //init homeVue
        //init spinnerVue
        ui.homeVue = new Vue({
          el: '#home',
          data: {
            visible: true
          }
        } );
        ui.spinnerVue = new Vue({
          el: '#spinner',
          data: {
            visible: false
          }
        } );
        ui.headerVue = new Vue({
          el: '#header-bloc',
          data: {
            visible: false,
            com_url: '',
            nb_anon: 0,
            nb_users: 0,
            wp_badge: '',
            wd_label: '',
            wp_length: 0,
            wp_url: '',
            wd_url: '',
            wv_banner: '',
            wv_url: '',
            wp_last_update: ''
          }
        } );

        ui.progressBlocVue = new Vue({
          el: '#progress-bloc',
          data: {
            visible: false
          }
        } );
        ui.imagesBlocVue = new Vue({
          el: '#images-bloc',
          data: {
            visible: false,
            images: [],
            commons_category: '',
            images_number: 0,
            images_in_commons: 9999,
            wp_last_update: ''
          },
          computed: {
            images_number_plural() {
                return this.images_number > 1 ? 's' : '';
            },
            random_images() {
              var n = 4,
                  result = new Array( n ),
                  len = this.images.length,
                  taken = new Array( len );
              if ( n > len )
                  return this.images;
              while (n--) {
                  var x = Math.floor(Math.random() * len);
                  result[ n ] = this.images[ x in taken ? taken[x] : x ];
                  taken[ x ] = --len;
              }
              return result;
            }
          },
        } );
        console.log( $( '.hidden' ) );
        $( '.hidden' ).removeClass( 'hidden' );
    };
    
    this.setHome = function() {
        ui.spinnerVue.visible = false;
        ui.headerVue.visible = false;
        ui.imagesBlocVue.visible = false;
        
        ui.homeVue.visible = true;
    };
    
    this.changePage = function( qid, promise ) {
        ui.qid = qid;
        ui.setSpinner();
        promise.then( ui.setTimeline );
    };
    
    this.setSpinner = function() {
        ui.homeVue.visible = false;
        ui.headerVue.visible = false;
        ui.imagesBlocVue.visible = false;
        
        ui.spinnerVue.visible = true;
    };
    
    this.setTimeline = function( data ) {
        ui.data = data;
        
        var wp_last_update = new Date( ui.data.wp_last_update * 1000 );
        
        ui.homeVue.visible = false;
        ui.spinnerVue.visible = false;
        
        // Display the page header
        ui.headerVue.com_url = "https://commons.wikimedia.org/wiki/Category:" + data.commons_category;
        ui.headerVue.nb_anon = data.anoncontributors;
        ui.headerVue.nb_users = data.registeredcontributors;
        ui.headerVue.wp_badge = data.wp_article.badge;
        ui.headerVue.wd_label = data.wd_label;
        ui.headerVue.wp_length = formatNumber(data.length);
        ui.headerVue.wp_url = data.wp_article.url;
        ui.headerVue.wd_url = "https://www.wikidata.org/wiki/" + ui.qid;
        ui.headerVue.wv_banner = data.wv_banner;
        ui.headerVue.wv_url = data.wv_article.url;
        ui.headerVue.wp_last_update = wp_last_update.toLocaleString();
        ui.headerVue.visible = true;
        
        // Display the images bloc
        ui.imagesBlocVue.images = data.images;
        ui.imagesBlocVue.commons_category = 'https://commons.wikimedia.org/wiki/Special:UploadWizard?categories=' + data.commons_category;
        ui.imagesBlocVue.images_number = parseInt( data.images_number );
        //ui.imagesBlocVue.images_in_commons = ... TODO
        ui.imagesBlocVue.visible = true;
    };
    
    return this.init();
}



$( function() {

    // Autocomplete
    window.autocomplete = new macommune.Autocomplete( '#search-input', '#navbar' );
    
    window.navigation = new macommune.Navigation();
    window.onpopstate = navigation.onpopstate;
} );


function formatNumber (num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ")
}
