macommune.MapSelector = function( nav ) {
    this.nav = nav;
    this.requestCounter = 0;
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
                ( mapSelector.geoJsonGroup !== undefined && mapSelector.geoJsonGroup.getLayers().length > 0 ? 'Cliquez sur une ville.' : 'Zoomez vers votre ville.' ));
        };
        mapSelector.helpControl.addTo( mapSelector.map );
        
        //Create the legend message
        mapSelector.legendControl = L.control( { position: 'bottomright' } );
        mapSelector.legendControl.onAdd = function ( map ) {
            this._div = L.DomUtil.create('div', 'help-control info legend'),
                grades = [ 0, 20, 40, 60, 80, 100 ],
                labels = [ 'peu avancé', '', '', '', '', 'très complet' ];

            // loop through our density intervals and generate a label with a colored square for each interval
            for (var i = 0; i < grades.length; i++) {
                var gradientColor = mapSelector.pickGradientColor( grades[ i ] ).join(',') 
                this._div.innerHTML +=
                    '<i style="background:rgb(' + gradientColor + '); background:rgba(' + gradientColor + ', 0.6);"></i> ' +
                    labels[ i ] + ( grades[ i + 1 ] ? '<br>' : '' );
            }
            
            $( this._div ).hide();

            return this._div;
        };
        mapSelector.legendControl.disabled = function ( shouldDisable ) {
            if ( shouldDisable ) {
                $( this._div ).hide();
            }
            else {
                $( this._div ).show();
            }
        };
        mapSelector.legendControl.addTo( mapSelector.map );
        
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
        rgb = mapSelector.pickGradientColor( feature.properties.avg );
        
        return {
            fillColor: 'rgb(' + rgb[ 0 ] + ', ' + rgb[ 1 ] + ', ' + rgb[ 2 ] + ')',
            color: '#336699',
        };
    }
    
    this.pickGradientColor = function( value ) {
        const color1 = [ 33, 150, 243 ],
              color2 = [ 244, 67, 54 ]
        var w = ( value / 100 ) * 2 - 1,
            w1 = ( w * 1 + 1 ) / 2,
            w2 = 1 - w1;
        return [ Math.round( ( color1[ 0 ] * w1 ) + ( color2[ 0 ] * w2 ) ),
                    Math.round( ( color1[ 1 ] * w1 ) + ( color2[ 1 ] * w2 ) ),
                    Math.round( ( color1[ 2 ] * w1 ) + ( color2[ 2 ] * w2 ) ) ];
    }

    //Clear properly all the geoJson layers
    this.clearGeoJson = function() {
        if ( mapSelector.geoJsonGroup !== undefined ) {
            mapSelector.geoJsonGroup.eachLayer( function ( layer ) {
                layer.off();
            } );
            mapSelector.geoJsonGroup.clearLayers();
            mapSelector.geoJsonGroup.remove();
            delete mapSelector.geoJsonGroup;
        }
    };

    this.onMapMove = function() {
        if ( mapSelector.map.getZoom() >= 7 ) {
            var bounds = mapSelector.map.getBounds();
            var requestID = ++mapSelector.requestCounter;
            $.getJSON( '/api/geoshape/' + bounds.getSouth()
                       + '/' + bounds.getNorth()
                       + '/' + bounds.getWest()
                       + '/' + bounds.getEast() )
            .then( function( data ) {
                if ( requestID === mapSelector.requestCounter ) {
                    mapSelector.selectedLayer = undefined;
                    mapSelector.clearGeoJson();
                    if ( data.features !== undefined && data.features.length > 0 ) {
                        mapSelector.geoJsonGroup = L.geoJSON( data, {
                            onEachFeature: mapSelector.onEachFeature,
                            style: mapSelector.colorizeGeoJson,
                        } );
                        mapSelector.geoJsonGroup.addTo( mapSelector.map );
                        if ( mapSelector.selectedLayer !== undefined ) {
                            mapSelector.selectedLayer.bringToFront();
                        }
                        mapSelector.legendControl.disabled( false );
                    }
                    else {
                        mapSelector.legendControl.disabled( true );
                    }
                }
                mapSelector.helpControl.update();
                delete data;
            } );
        }
        else {
            mapSelector.clearGeoJson();
            mapSelector.helpControl.update();
            mapSelector.legendControl.disabled( true );
        }
    };
    
    this.move = function( lat, lng ) {
        mapSelector.map.flyTo( [ lat, lng ], 12 );
        //mapSelector.map.setView( [ lat, lng ], 12 );
    };

    return this.init();
};

