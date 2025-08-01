import axios from 'axios';

// Création d'une instance axios pour effectuer des requettes vers le backend
const instance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Intercepte toutes les requêtes et y ajoute le token s'il existe
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default instance;