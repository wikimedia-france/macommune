macommune.MapSelector = function( nav ) {
    this.nav = nav;
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
        mapSelector.geoJsonGroup = L.geoJSON( { "type": "FeatureCollection", "features": [] }, {
            onEachFeature: mapSelector.onEachFeature,
            style: mapSelector.colorizeGeoJson,
        } );
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
        if ( feature.properties.qid === mapSelector.nav.qid ) {
            mapSelector.selectedLayer = layer;
        }
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
    
    this.colorizeGeoJson = function( feature ) {
        if ( feature.properties.qid === mapSelector.nav.qid ) {
            return {
                fillColor: '#f2aa2e',
                color: '#f2aa2e',
                weight: 6,
            };
        }
        console.log( feature.properties.avg );
        var w = ( feature.properties.avg / 100 ) * 2 - 1;
        var w1 = ( w * 1 + 1 ) / 2;
        var w2 = 1 - w1;
        var rgb = [ Math.round( (33 * w1) + (244 * w2) ),
                    Math.round( (150 * w1) + (67 * w2) ),
                    Math.round( (243 * w1) + (54 * w2) ) ];
        console.log(rgb)
        return {
            fillColor: 'rgb(' + rgb[ 0 ] + ', ' + rgb[ 1 ] + ', ' + rgb[ 2 ] + ')',
            color: '#336699',
        };
    }

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
                mapSelector.selectedLayer = undefined;
                mapSelector.clearFeatures( mapSelector.geoJsonGroup );
                mapSelector.geoJsonGroup.addData( data );
                if ( mapSelector.selectedLayer !== undefined ) {
                    mapSelector.selectedLayer.bringToFront();
                }
                mapSelector.helpControl.update();
            } );
        }
        else {
            mapSelector.clearFeatures( mapSelector.geoJsonGroup );
        }
    };
    
    this.move = function( lat, lng ) {
        mapSelector.map.flyTo( [ lat, lng ], 12 );
        //mapSelector.map.setView( [ lat, lng ], 12 );
    };

    return this.init();
};

