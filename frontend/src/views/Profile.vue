<template>
  <div class="profile-container">
    <h2>Mon profil</h2>

    <div v-if="loading" class="loading">Chargement des informations...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="profile-card">
      <p><strong>Prénom :</strong> {{ user.firstname }}</p>
      <p><strong>Nom :</strong> {{ user.lastname }}</p>
      <p><strong>Email :</strong> {{ user.email }}</p>
      <p><strong>Adresse :</strong> {{ user.address }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import User from '@/models/User'; // import du model User afin d'utiliser ses fonctions


// céation des constantes de l'application 
const user = ref({});
const loading = ref(true);
const error = ref('');


// Fonction de récupèration des indormations d'un utilisateur  
const userProfile = async () => {
  try {
    // requette pour récupèrer les donées du model
    const response = await User.userProfile();
   
    // récupèration et traitement de la response
    if (response.data.status) {
      user.value = response.data.data;
    } else {
      error.value = response.data.message;
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  }finally {
      loading.value = false;
  }
};

// Exécutes la fonction au moment où le composant est monté dans le DOM
onMounted(userProfile);
</script>


<!-- Import du style  -->
<style scoped>
@import '../assets/styles/profile-style.css';
</style>
