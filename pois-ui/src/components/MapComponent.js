import React, { useEffect } from 'react';
import 'ol/ol.css';
import { Map, View } from 'ol';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import { OSM, Vector as VectorSource } from 'ol/source';
import { fromLonLat } from 'ol/proj';
import { Style, Icon } from 'ol/style';
import { Point } from 'ol/geom';
import { Feature } from 'ol';

const MapComponent = () => {
  useEffect(() => {
    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        // center: fromLonLat([60.1699, 24.9384]),
        center: [60.1699, 24.9384],
        zoom: 2,
      }),
    });

    // Fetch POIs from the Django backend
    fetch('http://localhost:8000/api/pois/')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          const features = data.map(poi => {
            const feature = new Feature({
              geometry: new Point(fromLonLat([poi.longitude, poi.latitude])),
              name: poi.description,
            });
  
            feature.setStyle(
              new Style({
                image: new Icon({
                  src: 'path_to_icon.png', // TODO: Add path to an icon image
                  scale: 0.05,
                }),
              })
            );
  
            return feature;
          });

          const vectorSource = new VectorSource({
            features: features,
          });
  
          const vectorLayer = new VectorLayer({
            source: vectorSource,
          });

          map.addLayer(vectorLayer);  
        } else {
          console.error('Expected an array but got:', data);
        }
      })
      .catch(error => {
        console.error('Error fetching POIs:', error);
      });
  }, []);

  return <div id="map" style={{ width: '100%', height: '100vh' }}></div>;
};

export default MapComponent;
