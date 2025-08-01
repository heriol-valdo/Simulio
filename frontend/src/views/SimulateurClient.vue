<template>
  <div class="simalateur-list">
    <div class="header">
      <h2>Liste des simulations client {{ clientItem.firstname }} </h2>
    </div>
     
    <div class="search-bar">
      <input type="date" v-model="searchTerm" placeholder="Rechercher par date" />
    </div>
          
    <div class="custom-table-wrapper">
      <div v-if="filteredSimulateurs.length === 0" class="empty-state">
      Aucune donnée simulation disponible.
    </div>
    <table v-else class="table table-striped custom-table">
          
      <thead class="thead-dark">
        <tr>
          <th>Date création</th>
          <th>Prix du bien</th>
          <th>mensualite</th>
          <th>Salaire</th>
        </tr>
      </thead>
          
      <tbody>
        <tr v-for="simulateur in paginatedSimulateurs" :key="simulateur.id">
          <td>{{ formatDateSimple(simulateur.created_at) }}</td>
          <td>{{ simulateur.prixBien }}</td>
          <td>{{ simulateur.mensualite }}</td>
          <td>{{ simulateur.salaire_minimum }}</td>
        </tr>
      </tbody>
    </table>
    </div>
      
    <div class="pagination">
      <button :disabled="page === 1" @click="page--" class="previous">Précédent</button>
      <span>Page {{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="page++" class="next">Suivant</button>
    </div>
            
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router'; //import  instance du routeur pour effectuer des navigations 
import Simulateur from '@/models/Simulateur'; // import du model Simulateur afin d'utiliser ses fonctions
import showToast from '@/components/showToast';// Import du composant pour afficher des messages 
import Client from '@/models/Client' // import du model Client afin d'utiliser ses fonctions


// céation des constantes de l'application 
const route = useRoute();
const clientId = ref(route.params.clientId);
const page = ref(1);
const perPage = 5;
const simulateurs = ref([]);
const searchTerm = ref('');
const clientItem = ref({});


// Fonction pour récupèrer les  informations d'un client précis 
const ClientOne = async () => {
  try {
    // requette pour récupèrer les donées au model
    const response = await Client.clientOne(clientId.value);

     // récupèration et traitement de la response
    if (response.data.status) {
       clientItem.value = response.data.data;
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur', true);
  }
};


// Fonction pour récupèrer les  simulations d'un client précis 
const SimulateurAll = async () => {
  try {
    // requette pour récupèrer les donées au model
    const response = await Simulateur.simulateurAll(clientId.value);
   
    // récupèration et traitement de la response
    if (response.data.status) {
      simulateurs.value = response.data.data;
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur', true);
  }
};

// Fonction pour formater la date de créaion d'une simulation avant affichage
const formatDateSimple = (dateString) => {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Mois commence à 0
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}

//  filtrage et mise à jour automatique  du tableau simulateur après une recherche
const filteredSimulateurs = computed(() => {
  return simulateurs.value.filter(simulateur =>
    `${simulateur.created_at} ${simulateur.prixBien}`.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

// nombre total de pages nécessaires pour afficher tous les simulations d'un client précis
const totalPages = computed(() =>
  Math.ceil(filteredSimulateurs.value.length / perPage)
);

// calculer automatiquement la partie du tableau filtré à afficher sur la page courante
const paginatedSimulateurs = computed(() => {
  const start = (page.value - 1) * perPage;
  return filteredSimulateurs.value.slice(start, start + perPage);
});

// Observe la const searchTerm et remet la page courante à 1 
watch(searchTerm, () => {
  page.value = 1;
});

//observe la liste filtrée des simulations  et restreint le nombre de a page pour qu'il ne depasse pas le nombre total de pages possibles 
watch(filteredSimulateurs, () => {
  if (page.value > totalPages.value) {
    page.value = totalPages.value || 1;
  }
});

// Exécutes la fonction au moment où le composant est monté dans le DOM
onMounted(SimulateurAll);
onMounted(ClientOne);
</script>

<!-- Import du style  -->
<style scoped>
@import '../assets/styles/simulateur-client-style.css';
</style>