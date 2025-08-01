<template>
  <div class="register-container">
    <h2>
      <img src="../assets/images/simulio.svg" alt="register image" class="register-image" />
    </h2>
    <form @submit.prevent="userRegister">
      <input v-model="firstname" type="text" placeholder="Prénom" required />
      <input v-model="lastname" type="text" placeholder="Nom" required />
      <input v-model="address" type="text" placeholder="Adresse" required />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        required
        :class="{ invalid: emailError }"
      />

      <div class="password-container">
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Mot de passe"
          required
          :class="{ invalid: passwordError }"
        />
        <button
          type="button"
          class="toggle-password"
          @click="showPassword = !showPassword"
          :title="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
        >
          <span v-if="showPassword">
            <i class="fa fa-eye-slash" aria-hidden="true"></i>
          </span>
          <span v-else>
            <i class="fa fa-eye" aria-hidden="true"></i>
          </span>
        </button>
      </div>

      <button type="submit" :disabled="loading">
        <span v-if="loading">Enregistrement...</span>
        <span v-else>S'enregistrer</span>
      </button>
    </form>

    <button type="button" :disabled="loading" @click="router.push('/login')">
      <span>Se connecter</span>
    </button>

   
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; //import  instance du routeur pour effectuer des navigations 
import User from '@/models/User'; // import du model User afin d'utiliser ses fonctions
import showToast from '@/components/showToast';  // Import du composant pour afficher des messages 


// céation des constantes de l'application 
const firstname = ref('');
const lastname = ref('');
const address = ref('');
const email = ref('');
const password = ref('');
const emailError = ref(false);
const passwordError = ref(false);
const loading = ref(false);
const showPassword = ref(false);
const router = useRouter();



// Fonction d'enregistrement d'un utilisateur  
const userRegister = async () => {
  emailError.value = !email.value.trim();
  passwordError.value = !password.value.trim() || password.value.length < 8;

   // Vérification des champs du formulaire avant soumission 
  if (emailError.value || passwordError.value) {
    if (passwordError.value && password.value.length < 8) {
      showToast('Le mot de passe doit contenir au moins 8 caractères',true);
    } else {
      showToast('Veuillez remplir tous les champs correctement', true);
    }
    return;
  }

  loading.value = true;
  try {
    // requette pour envoyer les donées au model
    const response =  await User.userRegister(firstname.value, lastname.value, address.value, email.value, password.value);

    // récupèration et traitement de la response
    if (response.data.status) {
      showToast(response.data.message);
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  } finally {
    loading.value = false;
  }
};
</script>


<!-- Import du style  -->
<style scoped>
@import '../assets/styles/register-style.css';
</style>