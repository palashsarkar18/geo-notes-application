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
import Overlay from 'ol/Overlay';
import { getPOIs, createPOI, updatePOI, deletePOI } from '../services/poiService';
import { getCsrfToken } from '../utils/csrf';

const MapComponent = () => {
  const mapRef = useRef(null);
  const [vectorSource] = useState(new VectorSource());
  const [selectedFeature, setSelectedFeature] = useState(null);
  const token = localStorage.getItem('token');
  const popupRef = useRef(null);
  const contentRef = useRef(null);

  const handleMapClick = async (event) => {
    if (event.defaultPrevented) {
      return; // Prevents further propagation of the current event.
    }
    console.log("handleMapClick");
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
          description: newPOI.description,
          createdAt: newPOI.created_at,
          updatedAt: newPOI.updated_at,
          user: newPOI.user
        });
        feature.setId(newPOI.id);
        feature.setStyle(
          new Style({
            image: new Icon({
              src: '/geolocation_marker.png',
              scale: 1
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
    console.log("handlePointerMove");
    const map = mapRef.current;
    const selected = map.forEachFeatureAtPixel(event.pixel, (feature) => feature);

    if (selected) {
      if (selectedFeature !== selected) {
        setSelectedFeature(selected);
        map.getTargetElement().style.cursor = 'pointer';

        const coordinates = selected.getGeometry().getCoordinates();
        const description = selected.get('description');
        const createdAt = selected.get('createdAt');
        const updatedAt = selected.get('updatedAt');
        const user = selected.get('user');

        if (contentRef.current) {
          // TODO: Delete these lines
          // contentRef.current.innerHTML = `
          //   <p><strong>Description:</strong> ${description}</p>
          //   <p><strong>Created by:</strong> ${user}</p>
          //   <p><strong>Created at:</strong> ${createdAt}</p>
          //   <p><strong>Updated at:</strong> ${updatedAt}</p>
          //   <button id="edit-poi">Edit</button>
          //   <button id="delete-poi">Delete</button>
          // `;

          contentRef.current.innerHTML = description;

          // Use a timeout to ensure the DOM elements are rendered before accessing them
          setTimeout(() => {
            const editButton = document.getElementById('edit-poi');
            const deleteButton = document.getElementById('delete-poi');
            if (editButton) {
              editButton.onclick = (e) => {
                e.stopPropagation(); // Stop event propagation to prevent map click
                handleEditPOI();
              };
            }
            if (deleteButton) {
              deleteButton.onclick = (e) => {
                e.stopPropagation(); // Stop event propagation to prevent map click
                handleDeletePOI();
              };
            }
          }, 0);
        }
        if (popupRef.current) {
          popupRef.current.setPosition(coordinates);
        }
      }
    } else {
      if (selectedFeature) {
        setSelectedFeature(null);
        map.getTargetElement().style.cursor = '';
        if (popupRef.current) {
          popupRef.current.setPosition(undefined); // Hide the popup
        }
      }
    }
  };

  useEffect(() => {
    const popupElement = document.getElementById('popup');
    const contentElement = document.getElementById('popup-content');
    contentRef.current = contentElement;  // Set the contentRef to the actual DOM element
    popupRef.current = new Overlay({
      element: popupElement,
      positioning: 'bottom-center',
      stopEvent: false,
      offset: [0, -10]
    });

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
        }),
        overlays: [popupRef.current]
      });

      // Fetch POIs from the backend
      getPOIs(token).then(data => {
        if (Array.isArray(data)) {
          const features = data.map(poi => {
            const feature = new Feature({
              geometry: new Point(fromLonLat([poi.longitude, poi.latitude])),
              description: poi.description,
              createdAt: poi.created_at,
              updatedAt: poi.updated_at,
              user: poi.user
            });
            feature.setId(poi.id);
            feature.setStyle(
              new Style({
                image: new Icon({
                  src: '/geolocation_marker.png',
                  scale: 1
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

      mapRef.current.on('singleclick', handleMapClick);
      mapRef.current.on('pointermove', handlePointerMove);
    }

    return () => {
      if (mapRef.current) {
        // Cleanup event listeners
      }
    };
  }, [token]);

  const handleEditPOI = () => {
    if (selectedFeature) {
      const newDescription = prompt('Edit description for the POI:', selectedFeature.get('description'));
      if (newDescription) {
        const updatedPOI = { description: newDescription };
        updatePOI(token, selectedFeature.getId(), updatedPOI).then(() => {
          selectedFeature.set('description', newDescription);
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
      <div id="popup" className="ol-popup">
        <div id="popup-content" ref={contentRef}></div>
      </div>
    </div>
  );
};

export default MapComponent;
