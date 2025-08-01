import axios from '@/config/axios';
import User from '@/models/User';  // import du model User afin d'utiliser ses fonctions

export default {

 // Fonction pour exécuter une simulation
  async simulateur(data) {
    await User.requireValidToken();
    return await axios.post('/simulateur', data);
  },

   // Fonction pour  ajouter une simulation à un client
  async simulateurRegister(clientId, resultats) {
    const response = await axios.post('/simulateurRegister', {
      clientId,
      ...resultats
    });
    return response.data;
  },

  // Fonction pour rechercher les simulations d'un client précis
  async simulateurAll(id) {
    await User.requireValidToken();
    return await axios.get(`/simulateurAll/${id}`);
}
};


