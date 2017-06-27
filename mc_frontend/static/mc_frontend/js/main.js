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
    
        // TODO: Set the spinner
        
        nav.fetchData().then( function( data ) {
            // TODO: give that data to the vue interface
            $( '#app' ).text( nav.title );
            console.log( data );
            if ( changeHistory === true ) {
                history.pushState( { qid: nav.qid, title: nav.title }, '', '/' + nav.qid + '/' + nav.title );
            }
        } )
    }

    this.resetView = function() {
        nav.qid = null;
        nav.title = null;
        $( '#app' ).empty()
        // TODO: Reset the view
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



$( function() {

    // Autocomplete
    window.autocomplete = new macommune.Autocomplete( '#search-input', '#navbar' );
    
    window.navigation = new macommune.Navigation();
    window.onpopstate = navigation.onpopstate;
} );
