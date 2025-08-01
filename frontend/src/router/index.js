import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import AppLayout from '@/templates/AppLayout.vue';
import Clients from '@/views/Clients.vue';
import Simulateur from '@/views/Simulateur.vue';
import SimulateurClient from '@/views/SimulateurClient.vue';
import User from '@/models/User';
import Profile from '@/views/Profile.vue';


// créer les routes
const routes = [
  { 
    path: '/login',  // Uri pour accéder à la vue 
    name: 'Login',   // Nom symbolique de la route utiliser pour la redirection (routage)
    component: Login,
    meta: { title: ' Login' } //  titre de la page
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: Register,
    meta: { title: ' Register' } 
  },
  {
    path: '/',
    component: AppLayout, // compossant parent contenant la navbar, hearder et footer
    children: [
      {
        path: '/',
        name: 'Clients',
        component: Clients,  // composant parent greffer au composant parent 
        meta: { requiresAuth: true, title: ' Clients' }
      },
      {
        path: 'simulateur',
        name: 'Simulateur',
        component: Simulateur,
        meta: { requiresAuth: true, title: ' Simulateurs' }
      },
      {
        path: 'simulateurClient/:clientId', 
        name: 'SimulateurClient',
        component: SimulateurClient,
        meta: { requiresAuth: true, title: ' Simulations Client' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: { requiresAuth: true, title: ' Profile' }
      },
     
    ]
  },
  {
    path: '/:pathMatch(.*)*', // rediriger si aucune route n'est trouvée
    redirect: '/'
  }
];


// créer une nouvelle instance du routeur 
const router = createRouter({
  history: createWebHistory(),
  routes
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = User.isTokenValid();

  // vérifier si l'utilisateur avant d'accéder @ une route
  if (to.meta.requiresAuth && !isAuthenticated) {
    User.logout();
  }

  // rediriger l'utilisateur si déjà authentifier
  if (isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
    return next('/');
  }

  next();
});


// Ajouter un titre en fonction du fichier .vue
router.afterEach((to) => {
  const defaultTitle = 'Simulio |';
  document.title = defaultTitle + to.meta.title || defaultTitle;
});

export default router;