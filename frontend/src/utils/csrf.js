export const getCsrfToken = async () => {
  const response = await fetch('http://localhost:8000/api/csrf-token/', {
    credentials: 'include',  // Include credentials
  });
  const data = await response.json();
  return data.csrfToken;
};
