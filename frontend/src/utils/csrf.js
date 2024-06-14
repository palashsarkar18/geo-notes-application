const API_URL = process.env.REACT_APP_API_URL;

export const getCsrfToken = async () => {
  const response = await fetch(`${API_URL}/csrf-token/`, {
    credentials: 'include',  // Include credentials
  });
  const data = await response.json();
  return data.csrfToken;
};
