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
    
        if ( nav.ui !== undefined ) {
            nav.ui.destroy();
        }
        
        nav.ui = new macommune.Ui( nav.qid, nav.fetchData() );
        
        if ( changeHistory === true ) {
            history.pushState( { qid: nav.qid, title: nav.title }, '', '/' + nav.qid + '/' + nav.title );
        }
    }

    this.resetView = function() {
        nav.qid = null;
        nav.title = null;
        
        if ( nav.ui !== undefined ) {
            nav.ui.destroy();
            nav.ui = undefined;
        }
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

macommune.Ui = function( qid, promise ) {
    this.qid = qid;
    this.promise = promise;
    this.data = null;
    
    var ui = this;
    
    this.init = function() {
        if ( ui.promise === undefined ) {
            ui.setHome();
        }
        else {
            ui.setSpinner();
            promise.then( ui.setTimeline );
        }
    };
    
    this.setHome = function() {
        
    };
    
    this.setSpinner = function() {
        
    };
    
    this.setTimeline = function( data ) {
        //console.log( data )
        ui.data = data;
        
        var updated = new Date( ui.data.local_db.updated * 1000 );
        ui.vueApp = new Vue({
          el: '#app',
          data: {
            com_url: "https://commons.wikimedia.org/wiki/Category:" + data.commons_category,
            nb_anon: data.anoncontributors,
            nb_users: data.registeredcontributors,
            wp_badge: data.wp_article.badge,
            wd_label: data.wd_label,
            wp_weight: data.length,
            wp_url: data.wp_article.url,
            wd_url: "https://www.wikidata.org/wiki/" + ui.qid,
            wv_url: data.wv_article.url,
            updated: updated.toLocaleString()
          }
        });
    
    };
    
    this.destroy = function() {
        ui.vueApp.$destroy();
    };
    
    return this.init();
}



$( function() {

    // Autocomplete
    window.autocomplete = new macommune.Autocomplete( '#search-input', '#navbar' );
    
    window.navigation = new macommune.Navigation();
    window.onpopstate = navigation.onpopstate;
} );
