import axios from '@/config/axios';
import User from '@/models/User'; // import du model User afin d'utiliser ses fonctions

export default {

// Fonction pour récupèrer les clients 
  async clientAll() {
    await User.requireValidToken(); // Verification du token de l'utilisateur avant d'effectuer la requette 
    return await axios.get('/clientAll');
  },

  // Fonction pour  ajouter un client
  async clientRegister(clientData) {
    await User.requireValidToken();
    return await axios.post('/clientRegister', clientData);
  },

  // Fonction pour modifier un client
  async clientUpdate(id, clientData) {
    await User.requireValidToken();
    return await axios.put(`/clientUpdate/${id}`, clientData);
  },

  // Fonction pour  supprimer un client
  async clientDelete(id) {
    await User.requireValidToken();
    return await axios.delete(`/clientDelete/${id}`);
  },

  // Fonction pour  récupèrer les informations d'un client précis
  async clientOne(id) {
    await User.requireValidToken();
    return await axios.get(`/clientOne/${id}`);
  }
};
