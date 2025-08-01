import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App); // création instance de l'application
app.use(router); // ajout du gestionnaire de routage 
app.mount('#app');  // montage de l'instance dans le DOM de APP.vue

