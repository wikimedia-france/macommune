$( function() {

    //Initialise the map container
    var map = L.map('mapselector').setView([47, 1], 5);

    //Add a base layer, which contains no labels
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
        attribution: '©OpenStreetMap, ©CartoDB'
    }).addTo(map);

    //Add in a separated pane a layer containing only labels
    map.createPane('labels');
    map.getPane('labels').style.zIndex = 650;
    map.getPane('labels').style.pointerEvents = 'none';

    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png', {
        attribution: '©OpenStreetMap, ©CartoDB',
        pane: 'labels',
    }).addTo(map);

    //Add an empty geoJson layer group in between
    geoJsonGroup = L.geoJSON({ "type": "FeatureCollection", "features": []}, { onEachFeature: onEachFeature });
    geoJsonGroup.addTo(map);

    //Create a control which will contain little help messages
    var helpControl = L.control();
    helpControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'help-control');
        this.update();
        return this._div;
    };
    helpControl.update = function (title) {
        this._div.innerHTML = '<h4>Aide</h4>' +  ( title ?
            'Cliquez pour voir <b>' + title + '</b> en détail.'
            : ( geoJsonGroup.getLayers().length > 0 ? 'Cliquez sur une ville.' : 'Zoomez vers votre ville.' ));
    };
    helpControl.addTo(map);

    //Refresh the displayed geoJson polygons each times the map is moved
    map.on('moveend', function() {
        if ( map.getZoom() >= 9 ) {
            var bounds = map.getBounds();
            $.getJSON('http://127.0.0.1:8000/api/geoshape/'+bounds.getSouth()+'/'+bounds.getNorth()+'/'+bounds.getWest()+'/'+bounds.getEast()).then(function(data) {
                clearFeatures( geoJsonGroup );
                geoJsonGroup.addData( data );
                helpControl.update();
            });
        }
        else {
            clearFeatures( geoJsonGroup );
        }
    });

    //Add some events handlers to all new geojson polygon
    function onEachFeature( feature, layer ) {
        layer.on({
            mouseover: function() {
                helpControl.update( feature.properties.title );
            },
            mouseout: function() {
                helpControl.update();
            },
            click: function() {
                console.log( feature.properties.qid );
            }
        });
    }

    //Clear properly all the geoJson layers
    function clearFeatures( geoJsonGroup ) {
        geoJsonGroup.eachLayer(function (layer) {
            layer.off();
        } );
        geoJsonGroup.clearLayers();
        helpControl.update();
    }
} );
