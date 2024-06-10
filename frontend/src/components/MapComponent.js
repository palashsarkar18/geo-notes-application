import React, { useEffect } from 'react';
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import { Feature } from 'ol';
import { Point } from 'ol/geom';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { Style, Icon } from 'ol/style';

const MapComponent = () => {
  useEffect(() => {
    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM()
        })
      ],
      view: new View({
        center: fromLonLat([24.9384, 60.1699]),
        zoom: 12
      })
    });

    const token = localStorage.getItem('token');

    // Fetch POIs from the Django backend
    fetch('http://localhost:8000/api/pois/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (Array.isArray(data)) {
        const features = data.map(poi => {
          const feature = new Feature({
            geometry: new Point(fromLonLat([poi.longitude, poi.latitude])),
            name: poi.description
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: 'path_to_icon.png',
                scale: 0.05
              })
            })
          );

          return feature;
        });

        const vectorSource = new VectorSource({
          features: features
        });

        const vectorLayer = new VectorLayer({
          source: vectorSource
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

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      <div id="map" style={{ width: '100%', height: '100vh' }}></div>
    </div>
  );
};

export default MapComponent;
