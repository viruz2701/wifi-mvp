import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('🔵 Request:', {
    url: config.url,
    fullUrl: `${config.baseURL}${config.url}`,
    method: config.method,
    hasToken: !!token,
    headers: config.headers
  });
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


api.interceptors.response.use(
  (response) => {
    console.log('🟢 Response:', {
      url: response.config.url,
      status: response.status
    });
    return response;
  },
  (error) => {
    console.log('🔴 Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message
    });
    return Promise.reject(error);
  }
);

export default api;