window.macommune = {};

macommune.autocomplete = function( id, parentId ) {
    this.id = id;
    this.parentId = parentId;
    var cache = {};
    
    this.init = function() {
        $( this.id ).autocomplete( {
	        source: this.getData,
            select: this.onSelect,
            appendTo: this.parentId,
        } );
    }
    
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
    }
    
    this.onSelect = function( event, ui ) {
        loadPage( ui.item.qid, ui.item.value, true );
    }
    
    return this.init();
}




$( function() {

    // Autocomplete
    autocomplete = new macommune.autocomplete( '#search-input', '#navbar' );

    
    getParams = function() {
        var params = window.location.pathname.split( '/' );
        params.shift();
        return params
    }

    fetchData = function( qid ) {
        return $.get( '/api/item/' + qid )
    }

    initializePage = function() {
        var params = getParams();
        if ( params[ 0 ] === undefined || params[ 0 ] === '' ) {
            if ( resetView === true ) {
                resetView();
            }
            return;
        }
        macommune.loadPage( params[ 0 ], params[ 1 ] );
    }
    
    resetView = function() {
        $( '#app' ).empty()
        // TODO: Reset the view
    }
    
    loadPage = function( qid, pageName, changeHistory ) {
        // TODO: Set the spinner
        macommune.fetchData( qid ).then( function( data ) {
            // TODO: give that data to the vue interface
            $( '#app' ).text( pageName );
            console.log( data );
            if ( changeHistory === true ) {
                history.pushState( { qid: qid, pageName: pageName }, '', '/' + qid + '/' + pageName );
            }
        } )
    }
    
    onpopstate = function(event) {
        if ( event.state === null ) {
            macommune.initializePage()
            return;
        }
        
        loadPage( event.state.qid, event.state.pageName );
    };
    
    
    initializePage();

} );
