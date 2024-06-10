import React, { useEffect, useState, useRef } from 'react';
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat, toLonLat } from 'ol/proj';
import { Feature } from 'ol';
import { Point } from 'ol/geom';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { Style, Icon } from 'ol/style';
import { getPOIs, createPOI, updatePOI, deletePOI } from '../services/poiService';
import { getCsrfToken } from '../utils/csrf';

const MapComponent = () => {
  const mapRef = useRef(null);
  const [vectorSource] = useState(new VectorSource());
  const [selectedFeature, setSelectedFeature] = useState(null);
  const token = localStorage.getItem('token');

  const handleMapClick = async (event) => {
    console.log("I AM HERE 1 - handleMapClick");
    const coordinate = toLonLat(event.coordinate);
    const description = prompt('Enter description for the POI:');

    if (description) {
      const poi = { 
        latitude: parseFloat(coordinate[1].toFixed(6)), 
        longitude: parseFloat(coordinate[0].toFixed(6)),
        description 
      };
      console.log("Payload to be sent to the server:", poi);  // Log the payload

      // Fetch CSRF token
      const csrfToken = await getCsrfToken();
      console.log("CSRF Token:", csrfToken);


      createPOI(token, poi).then(newPOI => {
        const feature = new Feature({
          geometry: new Point(fromLonLat([newPOI.longitude, newPOI.latitude])),
          name: newPOI.description
        });
        feature.setId(newPOI.id);
        feature.setStyle(
          new Style({
            image: new Icon({
              src: 'path_to_icon.png',
              scale: 0.05
            })
          })
        );
        vectorSource.addFeature(feature);
      }).catch(error => {
        console.error('Error creating POI:', error);
      });
    }
  };

  const handlePointerMove = (event) => {
    console.log("I AM HERE 2 - handlePointerMove");

    const selected = mapRef.current.forEachFeatureAtPixel(event.pixel, (feature) => {
      return feature;
    });

    if (selected) {
      if (selectedFeature !== selected) {
        setSelectedFeature(selected);
        mapRef.current.getTargetElement().style.cursor = 'pointer';
      }
    } else {
      if (selectedFeature) {
        setSelectedFeature(null);
        mapRef.current.getTargetElement().style.cursor = '';
      }
    }
  };

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = new Map({
        target: 'map',
        layers: [
          new TileLayer({
            source: new OSM()
          }),
          new VectorLayer({
            source: vectorSource
          })
        ],
        view: new View({
          center: fromLonLat([24.9384, 60.1699]),
          zoom: 12
        })
      });

      // Fetch POIs from the backend
      getPOIs(token).then(data => {
        if (Array.isArray(data)) {
          const features = data.map(poi => {
            const feature = new Feature({
              geometry: new Point(fromLonLat([poi.longitude, poi.latitude])),
              name: poi.description
            });
            feature.setId(poi.id);
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
          vectorSource.addFeatures(features);
        } else {
          console.error('Expected an array but got:', data);
        }
      }).catch(error => {
        console.error('Error fetching POIs:', error);
      });

      console.log("Adding event listeners - singleclick and pointermove");
      mapRef.current.on('singleclick', handleMapClick);
      mapRef.current.on('pointermove', handlePointerMove);
      console.log("I AM HERE 3 - map initialized and event listeners added");
    }

    // Cleanup function to remove event listeners only when component unmounts
    return () => {
      if (mapRef.current) {
        // console.log("Removing event listeners - singleclick and pointermove");
        // mapRef.current.un('singleclick', handleMapClick);
        // mapRef.current.un('pointermove', handlePointerMove);
        // console.log("I AM HERE 4 - event listeners removed");
      }
    };
  }, [token]);

  const handleEditPOI = () => {
    if (selectedFeature) {
      const newDescription = prompt('Edit description for the POI:', selectedFeature.get('name'));
      if (newDescription) {
        const updatedPOI = { description: newDescription };
        updatePOI(token, selectedFeature.getId(), updatedPOI).then(() => {
          selectedFeature.set('name', newDescription);
        }).catch(error => {
          console.error('Error updating POI:', error);
        });
      }
    }
  };

  const handleDeletePOI = () => {
    if (selectedFeature) {
      if (window.confirm('Are you sure you want to delete this POI?')) {
        deletePOI(token, selectedFeature.getId()).then(() => {
          vectorSource.removeFeature(selectedFeature);
          setSelectedFeature(null);
        }).catch(error => {
          console.error('Error deleting POI:', error);
        });
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      <button onClick={handleEditPOI} disabled={!selectedFeature}>Edit Selected POI</button>
      <button onClick={handleDeletePOI} disabled={!selectedFeature}>Delete Selected POI</button>
      <div id="map" style={{ width: '100%', height: '100vh' }}></div>
    </div>
  );
};

export default MapComponent;
