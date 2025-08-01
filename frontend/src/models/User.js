import axios from '@/config/axios';
import showToast from '@/components/showToast'; // Import du composant pour afficher des messages 
import router from '@/router';//import  instance du routeur pour effectuer des navigations 

function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

export default {
    
  // Fonction de connexion d'un utilisateur
    async userLogin(email, password) {
    return await axios.post('/userLogin', { email, password });
  },

  // Fonction d'enregistrement d'un utilisateur  
  async userRegister(firstname,lastname,address,email, password) {
    return  await axios.post('/userRegister', { firstname,lastname,address,email, password });
  },

  // Fonction de récupèration des indormations d'un utilisateur  
  async userProfile() {
    await this.requireValidToken();
    return await axios.get('/userProfile');
  },
  
  // Fonction de deconnexion d'un utilisateur  
  logout(message = false) {
    localStorage.removeItem('token');
    if(message){
      showToast('Merci pour votre visite. Vous avez été déconnecté.');
    }else{
      showToast('Veuillez vous connecter pour accéder à cette page.', true);
    }

    router.push('/login');
  },

 // Fonction pour vérifier si un token est valide
  isTokenValid() {
    const token = localStorage.getItem('token');
    if (!token) return false;

    const payload = parseJwt(token);
    if (!payload || !payload.exp) return false;

    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime;
  },

 // Fonction pour vérifier un token et gérer la redirection
  async requireValidToken() {
    if (!this.isTokenValid()) {
      this.logout(false); 
    }
  }
 
};


