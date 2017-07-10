window.macommune = {};

macommune.Autocomplete = function( nav, id, parentId ) {
    this.nav = nav;
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
};


macommune.Navigation = function() {
    this.qid = null;
    this.title = null;
    this.searchInput = $( '#search-input' );
    this.ui;
    this.mapSelector;
    this.autocomplete;
    
    var nav = this;

    this.init = function() {
        var params = nav.getParams();
        
        if ( nav.ui === undefined ) {
            nav.mapSelector = new macommune.MapSelector( nav );
            nav.autocomplete = new macommune.Autocomplete( nav, '#search-input', '#navbar' );
            nav.ui = new macommune.Ui( nav, params[ 0 ] );
            window.onpopstate = nav.onpopstate;
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
        
        nav.searchInput.val( decodeURI( title ) );
        
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
};

macommune.Ui = function( nav, qid ) {
    this.nav = nav;
    this.qid = qid;
    this.data = null;
    this.homeVue;
    this.spinnerVue;
    this.blocs;
    
    var ui = this;
    
    this.init = function() {
        console.log( 'new UI initialised' )
        if ( ui.qid === undefined ) {
            ui.setHome();
        }
        
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
        
        ui.blocs = new macommune.Blocs();
        
        $( '.hidden' ).removeClass( 'hidden' );
    };
    
    this.setHome = function() {
        ui.spinnerVue.visible = false;
        ui.blocs.hideAll();
        
        ui.homeVue.visible = true;
    };
    
    this.changePage = function( qid, promise ) {
        ui.qid = qid;
        ui.setSpinner();
        promise.then( ui.setTimeline );
    };
    
    this.setSpinner = function() {
        ui.homeVue.visible = false;
        ui.blocs.hideAll();
        
        ui.spinnerVue.visible = true;
    };
    
    this.setTimeline = function( data ) {
        ui.data = data;

        ui.homeVue.visible = false;
        ui.spinnerVue.visible = false;
        
        ui.blocs.setHeader( data );
        
        if ( data.latlng !== undefined ) {
            ui.nav.mapSelector.move( data.latlng.latitude, data.latlng.longitude );
        }
        
        if ( data.local_db.local_db !== false ) {
            ui.blocs.setProgress( data );
        }
        ui.blocs.setImages( data );
    };
    
    return this.init();
};


function formatNumber (num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ")
};


$( function() {
    window.navigation = new macommune.Navigation();
} );
