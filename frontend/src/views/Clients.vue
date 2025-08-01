<template>
  <div class="client-list">
    <div class="header">
      <h2>Liste des clients</h2>
      <button class="add-btn" @click="showAddModal = true">
        <i class="fas fa-plus"></i> Ajouter un client
      </button>
    </div>

    <div class="search-bar">
      <input v-model="searchTerm" placeholder="Rechercher par nom..." />
    </div>

    

    <div class="custom-table-wrapper">
      <div v-if="filteredClients.length === 0" class="empty-state">
      Aucune donnée client disponible.
    </div>
    <table v-else class="table table-striped custom-table">
          <thead class="thead-dark">
            <tr>
              <th>Prénom</th>
              <th>Nom</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="client in paginatedClients" :key="client.id">
              <td>{{ client.firstname }}</td>
              <td>{{ client.lastname }}</td>
              <td>{{ client.email }}</td>
              <td class="client-actions">
                <button @click="openEditModal(client)" class="icon-button" title="Modifier">
                  <i class="fas fa-edit" ></i>
                </button>
                <button @click="confirmDelete(client)" class="icon-button-delete" title="Supprimer">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button @click="goToClientSimulations(client.id)" class="icon-button-file" title="Liste Simulations">
                  <i class="fa fa-file" ></i>
                </button>
              </td>
            </tr>
          </tbody>
    </table>
    </div>


    <div class="pagination">
      <button :disabled="page === 1" @click="page--" class="previous">Précédent</button>
      <span>Page {{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="page++" class="next">Suivant</button>
    </div>

    <!-- Modal d'ajout -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h3>Ajouter un client</h3>
        <form @submit.prevent="clientRegister">
          <input v-model="newClient.firstname" placeholder="Prénom" required />
          <input v-model="newClient.lastname" placeholder="Nom" required />
          <input v-model="newClient.address" placeholder="Adresse" required />
          <input v-model="newClient.number" placeholder="Téléphone" required />
          <input v-model="newClient.email" placeholder="Email" required />
          <div class="modal-actions">
            <button type="submit">Ajouter</button>
            <button type="button" @click="resetAddModal" class="button">Annuler</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de modification -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>Modifier client</h3>
        <form @submit.prevent="clientUpdate">
          <input v-model="editClient.firstname" placeholder="Prénom" required />
          <input v-model="editClient.lastname" placeholder="Nom" required />
          <input v-model="editClient.address" placeholder="Adresse" required />
          <input v-model="editClient.number" placeholder="Téléphone" required />
          <input v-model="editClient.email" placeholder="Email" required />
          <div class="modal-actions">
            <button type="submit">Mettre à jour</button>
            <button type="button" @click="resetEditModal" class="button">Annuler</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de suppression -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <h3>Confirmer la suppression</h3>
        <p>Voulez-vous vraiment supprimer {{ clientToDelete.firstname }} {{ clientToDelete.lastname }} ?</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="button">Non</button>
          <button @click="clientDelete" type="submit">Oui</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import Client from '@/models/Client';  // import du model Client afin d'utiliser ses fonctions
import showToast from '@/components/showToast'; // Import du composant pour afficher des messages 
import { useRouter } from 'vue-router';  //import  instance du routeur pour effectuer des navigations 


// céation des constantes de l'application 
const clients = ref([]);
const page = ref(1);
const perPage = 5;
const router = useRouter();

const showAddModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);

const newClient = ref({ firstname: '', lastname: '', address: '', number: '', email: '' });
const editClient = ref({});
const clientToDelete = ref(null);
const searchTerm = ref('');

// Fonction pour récupèrer les clients 
const clientAll = async () => {
  try {
    // requette pour récupèrer les donées au model
    const response = await Client.clientAll();

    // récupèration et traitement de la response
    if (response.data.status) {
      clients.value = response.data.data;
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  }
};

// Fonction pour  ajouter un client
const clientRegister = async () => {
  try {
     // requette pour récupèrer les donées au model
    const response = await Client.clientRegister({ ...newClient.value });
    
     // récupèration et traitement de la response
    if (response.data.status) {
      showToast(response.data.message);
      resetAddModal();
      await clientAll();
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  }
};

// Ouvrir la modal pour modifier un client
const openEditModal = (client) => {
  editClient.value = { ...client };
  showEditModal.value = true;
};

// Fonction pour modifier un client
const clientUpdate = async () => {
  try {
    const response = await Client.clientUpdate(editClient.value.id, editClient.value);
    if (response.data.status) {
      showToast(response.data.message);
      resetEditModal();
      await clientAll();
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  }
};

// Ouvrir la modal pour  supprimer un client
const confirmDelete = (client) => {
  clientToDelete.value = client;
  showDeleteModal.value = true;
};


// Fonction pour  supprimer un client
const clientDelete = async () => {
  try {
    const response = await Client.clientDelete(clientToDelete.value.id);
    if (response.data.status) {
      showToast(response.data.message);
      showDeleteModal.value = false;
      await clientAll();
    } else {
      showToast(response.data.message, true);
    }
  } catch (error) {
    showToast(error.response?.data?.message || 'Erreur réseau ou serveur.', true);
  }
};

//  réinitialisé la modal pour ajouter un client
const resetAddModal = () => {
  showAddModal.value = false;
  newClient.value = { firstname: '', lastname: '', address: '', number: '', email: '' };
};

// réinitialisé la modal pour modifier un client
const resetEditModal = () => {
  showEditModal.value = false;
  editClient.value = {};
};

//  fonction pour rechercher un client par son nom et prénom 
const filteredClients = computed(() => {
  return clients.value.filter(client =>
    `${client.firstname} ${client.lastname}`.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

// nombre total de pages nécessaires pour afficher tous les simulations d'un client précis
const totalPages = computed(() => Math.ceil(filteredClients.value.length / perPage));

// calculer automatiquement la partie du tableau filtré à afficher sur la page courante
const paginatedClients = computed(() => {
  const start = (page.value - 1) * perPage;
  return filteredClients.value.slice(start, start + perPage);
});

// Observe la const searchTerm et remet la page courante à 1 
watch(searchTerm, () => {
  page.value = 1;
});

//observe la liste filtrée des simulations  et restreint le nombre de a page pour qu'il ne depasse pas le nombre total de pages possibles 
watch(filteredClients, () => {
  if (page.value > totalPages.value) {
    page.value = totalPages.value || 1;
  }
});

// Fonction pour rediriger vers la page SimulateurClient 
const goToClientSimulations = (clientId) => {
  router.push({
    name: 'SimulateurClient',
    params: { clientId }
  });
};

// Exécutes la fonction au moment où le composant est monté dans le DOM
onMounted(clientAll);
</script>

<!-- Import du style  -->
<style scoped>
@import '../assets/styles/client-style.css';
</style>
