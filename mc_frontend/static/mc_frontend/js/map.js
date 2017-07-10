macommune.MapSelector = function() {
    this.map;

    var mapSelector = this;

    this.init = function() {
        // Initialise the main map object
        mapSelector.map = L.map( 'mapselector' ).setView( [ 46.85, 2 ], 6 );
        
        //Add a base layer, which contains no labels
        L.tileLayer( 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png', {
            attribution: '©OpenStreetMap, ©CARTO'
        } ).addTo( mapSelector.map );
        
        //Add in a separated pane a layer containing only labels
        mapSelector.map.createPane('labels');
        mapSelector.map.getPane('labels').style.zIndex = 650;
        mapSelector.map.getPane('labels').style.pointerEvents = 'none';

        L.tileLayer( 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_only_labels/{z}/{x}/{y}.png', {
            attribution: '©OpenStreetMap, ©CARTO',
            pane: 'labels',
        }).addTo( mapSelector.map );
        
        //Add an empty geoJson layer group in between
        mapSelector.geoJsonGroup = L.geoJSON( { "type": "FeatureCollection", "features": [] }, { onEachFeature: mapSelector.onEachFeature } );
        mapSelector.geoJsonGroup.addTo( mapSelector.map );
        
        //Create a control which will contain little help messages
        mapSelector.helpControl = L.control();
        mapSelector.helpControl.onAdd = function ( map ) {
            this._div = L.DomUtil.create( 'div', 'help-control' );
            this.update();
            return this._div;
        };
        mapSelector.helpControl.update = function ( title ) {
            this._div.innerHTML = '<h4>Aide</h4>' +  ( title ?
                'Cliquez pour voir <b>' + title + '</b> en détail.' :
                ( mapSelector.geoJsonGroup.getLayers().length > 0 ? 'Cliquez sur une ville.' : 'Zoomez vers votre ville.' ));
        };
        mapSelector.helpControl.addTo( mapSelector.map );
        
        //Refresh the displayed geoJson polygons each times the map is moved
        mapSelector.map.on( 'moveend', mapSelector.onMapMove );
    };

    //Add some events handlers to all new geojson polygon
    this.onEachFeature = function( feature, layer ) {
        layer.on( {
            mouseover: function() {
                mapSelector.helpControl.update( feature.properties.title );
            },
            mouseout: function() {
                mapSelector.helpControl.update();
            },
            click: function() {
                navigation.loadPage( feature.properties.qid, feature.properties.title, true );
            }
        } );
    };

    //Clear properly all the geoJson layers
    this.clearFeatures = function( geoJsonGroup ) {
        mapSelector.geoJsonGroup.eachLayer( function ( layer ) {
            layer.off();
        } );
        mapSelector.geoJsonGroup.clearLayers();
        mapSelector.helpControl.update();
    };

    this.onMapMove = function() {
        if ( mapSelector.map.getZoom() >= 9 ) {
            var bounds = mapSelector.map.getBounds();
            $.getJSON( '/api/geoshape/' + bounds.getSouth()
                       + '/' + bounds.getNorth()
                       + '/' + bounds.getWest()
                       + '/' + bounds.getEast() )
            .then( function( data ) {
                mapSelector.clearFeatures( mapSelector.geoJsonGroup );
                mapSelector.geoJsonGroup.addData( data );
                mapSelector.helpControl.update();
            } );
        }
        else {
            mapSelector.clearFeatures( mapSelector.geoJsonGroup );
        }
    };

    return this.init();
};

