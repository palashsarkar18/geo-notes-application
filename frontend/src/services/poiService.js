const API_URL = 'http://localhost:8000/api/pois';

export const getPOIs = async (tokenX, poi, csrfToken) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/pois/`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`,
    //   'X-CSRFToken': csrfToken  // Include CSRF token if necessary
    }
  });
  if (!response.ok) {
    throw new Error('Failed to fetch POIs');
  }
  return response.json();
};

export const createPOI = async (tokenX, poi, csrfToken) => {
  const token = localStorage.getItem('token');
  console.log("Sending POI data:", poi);  // Log the payload before sending it
  const response = await fetch(`${API_URL}/pois/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`,
      'X-CSRFToken': csrfToken  // Include CSRF token if necessary (TODO)

    },
    body: JSON.stringify(poi) // Ensure body is JSON string
  });

  console.log("Request Headers:", {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  });
  console.log("Request Body:", JSON.stringify(poi));

  if (!response.ok) {
    const errorData = await response.json();
    console.error("Error response from server:", errorData);  // Log server error response
    throw new Error('Failed to create POI');
  }
  return response.json();
};

export const updatePOI = async (id, poi) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/pois/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify(poi)
  });
  if (!response.ok) {
    throw new Error('Failed to update POI');
  }
  return response.json();
};

export const deletePOI = async (id) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/pois/${id}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  if (!response.ok) {
    throw new Error('Failed to delete POI');
  }
};
