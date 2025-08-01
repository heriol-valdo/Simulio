<template>
    <nav
      class="sidebar"
      :class="{
        'sidebar-collapsed': (!isMobile && isCollapsed) || (isMobile && !isMobileMenuOpen),
        'sidebar--mobile-open': isMobile && isMobileMenuOpen
      }"
    >


    <!-- Toggle button pour mobile -->
    <button class="toggle-btn" @click="toggleSidebar">
      <i class="fas fa-bars"></i>
    </button>

    <div class="logo">
      <h1 v-if="(isMobile && isMobileMenuOpen) || (!isMobile && !isCollapsed)">
        <img src="../assets/images/simulio.svg" alt="nav image" class="nav-image">
      </h1>
      <h1 v-else class="logo-mini"><img src="../assets/images/favicon.png" alt="nav image" class="nav-image-close"></h1>
    </div>
    
    <ul class="menu">
      <router-link to="/simulateur" class="link" @click="closeMobileMenu">
        <li class="menu-item" :class="{ active: $route.path === '/simulateur'  }" title="Simulateur">
          <i class="fas fa-chart-line icon"></i>
          <span v-if="(isMobile && isMobileMenuOpen) || (!isMobile && !isCollapsed)">SIMULATEUR</span>
        </li>
      </router-link>
      
      <router-link to="/" class="link" @click="closeMobileMenu">
        <li class="menu-item" :class="{ active: $route.path === '/' || $route.path ==='/profile' || $route.path.startsWith('/simulateurClient') }" title="Mes clients">
          <i class="fas fa-users icon"></i>
          <span v-if="(isMobile && isMobileMenuOpen) || (!isMobile && !isCollapsed)">MES CLIENTS</span>
        </li>
      </router-link>
      
    </ul>
    
    <div class="profile-section">
      <button class="profile-btn" @click="goToProfile" title="Mon profil">
        <i class="fas fa-user icon"></i>
        <span v-if="(isMobile && isMobileMenuOpen) || (!isMobile && !isCollapsed)">Mon profil</span>
      </button>
      
      <button class="logout-btn" @click="logout" title="Déconnexion">
        <i class="fas fa-sign-out-alt icon"></i>
        <span v-if="(isMobile && isMobileMenuOpen) || (!isMobile && !isCollapsed)">Déconnexion</span>
      </button>
    </div>

    <!-- Overlay pour mobile -->
    <div v-if="isMobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </nav>
</template>

<script setup>
import { ref,  onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router' //import  instance du routeur pour effectuer des navigations 
import User from '@/models/User' // import du model User afin d'utiliser ses fonctions

// céation des constantes de l'application 
const router = useRouter()
const isCollapsed = ref(false)
const isMobile = ref(window.innerWidth <= 768)
const isMobileMenuOpen = ref(false)
const previousScreenIsMobile = ref(isMobile.value)

// Détection d'écran
const handleResize = () => {
  const wasMobile = previousScreenIsMobile.value
  isMobile.value = window.innerWidth <= 768

  // Changement desktop pour mobile
  if (!wasMobile && isMobile.value) {
    // CAS 1 : sidebar était ouverte ,on la ferme
    if (!isCollapsed.value) {
      isMobileMenuOpen.value = false
    }
    // CAS 2 : sidebar était déjà fermée , elle reste fermée
  }

  // Changement mobile pour desktop , ne rien changer, on garde l’état collap
  previousScreenIsMobile.value = isMobile.value
}

// Fonction pour modifier l’état d’affichage de la sidebar.
const toggleSidebar = () => {
  if (isMobile.value) {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  } else {
    isCollapsed.value = !isCollapsed.value
  }
}

// fonction pour fermer le menu 
const closeMobileMenu = () => {
  if (isMobile.value) {
    isMobileMenuOpen.value = false
  }
}

// Rediriger vers le profil
const goToProfile = () => {
  router.push('/profile')
  closeMobileMenu()
}

// Deconnexion
const logout = () => {
  User.logout(true)
  closeMobileMenu()
}


// Exécutes la fonction au moment où le composant est monté dans le DOM
onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize()
})

// Exécutes la fonction au moment où le composant est retiré dans le DOM
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>


<!-- Import du style  -->
<style scoped>
@import '../assets/styles/navbar-style.css';
</style>
