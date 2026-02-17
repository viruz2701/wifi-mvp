import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1', // относительный путь, будет проксироваться Vite
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
    
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;