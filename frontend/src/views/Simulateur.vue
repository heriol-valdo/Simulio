<template>
 <div class="simulateur-container">
 
  <div class="form-section">
    <div class="form-title">
      <label>Achat en résidence principale dans l'ancien</label>
    </div>

    <div class="form-group-general">
      <!-- Champs sliders -->
      <div
        v-for="(field, key) in sliders"
        :key="key"
        class="form-group"
      >
        <label :for="key">{{ field.label }}</label>
        <div class="range-row">
          <input
            :id="key"
            type="range"
            v-model.number="form[key]"
            :min="field.min"
            :max="field.max"
            :step="field.step"
          />
          <input
            type="number"
            v-model.number="form[key]"
            :step="field.step"
            class="input-number"
            required
          />
          <span class="unit">{{ field.unit }}</span>
        </div>
      </div>

      <!-- Taux d'agence -->
      <div class="form-group form-number">
        <label class="label-form-agence">Frais d'agence</label>
        <input
          type="number"
          class="input-number-form"
          v-model="form.tauxFraisAgence"
        />
        <span class="unit form-number-unit">%</span>
      </div>

      <!-- Taux de notaire -->
      <div class="form-group form-number">
        <label class="label-form-notaire">Frais de notaire</label>
        <input
          type="number"
          class="input-number-form"
          min="0"
          max="15"
          step="0.1"
          v-model="form.tauxFraisNotaire"
        />
        <span class="unit form-number-unit">%</span>
      </div>

      <!-- Taux d'intérêt -->
      <div class="form-group form-number">
        <label class="label-form">Taux d'intérêt</label>
        <input
          type="number"
          class="input-number-form"
          min="0"
          max="10"
          step="0.01"
          v-model="form.tauxInteret"
        />
        <span class="unit form-number-unit">%</span>
      </div>

      <!-- Taux d'assurance -->
      <div class="form-group form-number">
        <label class="label-form-assurance">Taux d'assurance</label>
        <input
          type="number"
          class="input-number-form"
          min="0"
          max="5"
          step="0.01"
          v-model="form.tauxAssurance"
        />
        <span class="unit form-number-unit">%</span>
      </div>

      <!-- Taux Revalorisation annuelle -->
      <div class="form-group form-number">
        <label class="label-form-revalo">Revalorisation du bien par an </label>
        <input
          type="number"
          class="input-number-form"
          min="0"
          max="10"
          step="0.1"
          v-model="form.tauxRevalorisation"
        />
        <span class="unit form-number-unit">%</span>
      </div>

      <!-- Date d'acquisition -->
      <div class="form-group date-picker">
        <label>Date d'acquisition</label>
        <input type="month" v-model="form.dateAcquisition" />
      </div>

      <!-- Bouton de simulation -->
      <!-- <button @click="simulateur" :disabled="loading">
        {{ loading ? 'Simulation...' : 'Lancer la simulation' }}
      </button> -->
    </div>
  </div>

 
    <div class="result-section">


      <div class="form-title">
        <label>Resultat de simulation</label>
      </div>

     

      <div class="form-group-general">
      
          <div class="result-section-wrapper">

            <transition name="fade">
              <div v-if="loadingResultats" class="loader-overlay">
                <div class="bounce-loader">
                  <div></div><div></div><div></div>
                </div>
              </div>
            </transition>
            <h3>Votre mensualité sera de</h3>
            <div class="monthly">{{ formatEuro(resultats.mensualite) }} €</div>

            <table class="table-lignes">
              <tbody>
                <tr><td>Prix du bien</td><td>{{ formatEuro(resultats.prixBien) }} €</td></tr>
                <tr><td>Frais de notaire</td><td>{{ formatEuro(resultats.frais_notaire) }} €</td></tr>
                <tr><td>Garantie bancaire</td><td>{{ formatEuro(resultats.garantie_bancaire) }} €</td></tr>
                <tr><td>Travaux</td><td>{{ formatEuro(resultats.travaux) }} €</td></tr>
                <tr><td>Frais d'agence</td><td>{{ formatEuro(resultats.frais_agence_calcule) }} €</td></tr>
                <tr><td>Total à financer</td><td>{{ formatEuro(resultats.montant_finance) }} €</td></tr>
                <tr><td>Revenu acquéreur minimum mensuel</td><td>{{ formatEuro(resultats.salaire_minimum) }} €</td></tr>
              </tbody>
            </table>
          </div>


      
          <div class="form-group form-client">
            <label>Attribuer à un client :</label>
            <select v-model="selectedClientId">
              <option disabled value="">Choisir un client</option>
              <option
                v-for="client in clients"
                :key="client.id"
                :value="client.id"
              >
                {{ client.firstname }} {{ client.lastname }}
              </option>
            </select>
          </div>

    
          <button 
            @click="simulateurRegister" 
            :disabled="!resultats.mensualite || !selectedClientId"
          >
            Enregistrer la simulation
          </button>
      </div>
     
    </div>

 

</div>

</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import Simulateur from '@/models/Simulateur'; // import du model Simulateur afin d'utiliser ses fonctions
import Client from '@/models/Client'; // import du model Client afin d'utiliser ses fonctions
import showToast from '@/components/showToast'; // Import du composant pour afficher des messages 


// céation des constantes de l'application 
const loading = ref(false);
const loadingResultats = ref(false);
const selectedClientId = ref('');
const clients = ref([]);
const resultats = ref({
  prixBien: 0,
  mensualite: 0,
  interets: 0,
  assurance_totale: 0,
  frais_notaire: 0,
  garantie_bancaire: 0,
  salaire_minimum: 0,
  montant_finance: 0,
  frais_agence_calcule: 0,
  travaux: 0,
  tableau_amortissement: [],
  details_financement: [],
  details_credit: [],
  dates_financement: [],
  revente_simulee: {}
});
const form = reactive({
  prixBien: 834000,
  travaux: 20000,
  tauxFraisAgence: 3,
  duree: 25,
  apport: 50000, 
  tauxFraisNotaire: 7.5,
  tauxInteret: 3.5,
  tauxAssurance: 0.32,
  tauxRevalorisation: 1,
  dateAcquisition: '2024-01', // Date par défaut
  mois: 1,
  annee: 2024,
});

// Observe pour mettre à jour mois/annee quand dateAcquisition change
watch(() => form.dateAcquisition, (newDate) => {
  if (newDate && newDate.includes('-')) {
    const [annee, mois] = newDate.split('-');
    form.mois = parseInt(mois);
    form.annee = parseInt(annee);
  }
}, { immediate: true });

const sliders = {
  prixBien: { label: 'Prix du bien', min: 50000, max: 1500000, step: 1000, unit: '€' },
  travaux: { label: 'Travaux', min: 0, max: 200000, step: 1000, unit: '€' },
  duree: { label: 'Durée du prêt', min: 5, max: 30, step: 1, unit: 'ans' },
  apport: { label: 'Apport', min: 0, max: 500000, step: 1000, unit: '€' }
};

// Fonction pour formater la valeur passée en paramètre 
const formatEuro = (val) => {
  if (!val || isNaN(val)) return '0';
  return new Intl.NumberFormat('fr-FR').format(Math.round(val));
};


// Fonction pour lancer la simulation
const simulateur = async () => {
  const start = Date.now();
  loadingResultats.value = true;
  loading.value = true;
  
  try {
    //Crée une copie  de l'objet form pour que les modifications apportées n'inpactent pas la requette en cours 
    const formData = { ...form };

    // requette pour envoyer les donées au model
    const response = await Simulateur.simulateur(formData);
    
    // Calculer le temps écoulé depuis le début
    const elapsed = Date.now() - start;
    
    // S'assurer qu'au minimum 3 secondes se sont écoulées avant de traiter la réponse
    const minimumDelay = Math.max(0, 3000 - elapsed);
    
    setTimeout(() => {
       // récupèration et traitement de la response
      if (response.data.status) {
          resultats.value = {
            prixBien: response.data.data[0].prixBien || 0,
            mensualite: response.data.data[0].mensualite || 0,
            interets: response.data.data[0].interets || 0,
            assurance_totale: response.data.data[0].assurance_totale || 0,
            frais_notaire: response.data.data[0].frais_notaire || 0,
            garantie_bancaire: response.data.data[0].garantie_bancaire || 0,
            salaire_minimum: response.data.data[0].salaire_minimum || 0,
            montant_finance: response.data.data[0].montant_finance || 0,
            frais_agence_calcule: response.data.data[0].frais_agence_calcule || 0,
            tableau_amortissement: response.data.data[0].tableau_amortissement || [],
            details_financement: response.data.data[0].details_financement || [],
            details_credit: response.data.data[0].details_credit || [],
            dates_financement: response.data.data[0].dates_financement || [],
            revente_simulee: response.data.data[0].revente_simulee || {},
            travaux: response.data.data[0].travaux || 0
          };
        // showToast(response.data.message);
      } else {
        // showToast(response.data.message || 'Erreur lors de la simulation.', true);
      }
      
      // Suppression du loader après deux secondes quand la requette est terminée
      setTimeout(() => {
        loadingResultats.value = false;
        loading.value = false;
      }, 2000);
      
    }, minimumDelay);
    
  } catch (error) {
    console.error('Erreur simulation:', error);
    
    // En cas d'erreur, s'assurer que le loader tourne deux secondes
    const elapsed = Date.now() - start;
    const minimumDelay = Math.max(0, 2000 - elapsed);
    
    setTimeout(() => {
      loadingResultats.value = false;
      loading.value = false;
    }, minimumDelay);
  }
};



// Fonction pour attribuer une simulation à un client précis 
const simulateurRegister = async () => {

  // Vérifier si un client est sélectionner  
  if (!selectedClientId.value) {
    showToast('Veuillez sélectionner un client.', true);
    return;
  }
  
  try {
     // requette pour envoyer les donées au model
    await Simulateur.simulateurRegister(selectedClientId.value, resultats.value);

    showToast('Simulation enregistrée avec succès.');
  } catch (error) {
     showToast(error.response?.data?.message || 'Erreur réseau ou serveur', true);
  }
};

// Fonction pour récuperer l'ensemble des clients de l'utilisateur 
const fetchClients = async () => {
  try {
     // requette pour récupèrer les donées au model
    const res = await Client.clientAll();

    // récupèration et traitement de la response
    const data = res?.data?.data;
    if (!Array.isArray(data)) {
      showToast('Données des clients invalides.', true);
      return;
    }
    const validClients = data.filter(client => 
      client && 
      client.id && 
      typeof client.id === 'number' && 
      client.id > 0 &&
      client.firstname &&
      client.lastname
    );
    
    if (validClients.length === 0) {
      //showToast('Aucun client valide trouvé.', true);
      return;
    }
    
    clients.value = validClients;
  } catch (error) {
    console.error('Erreur fetch clients:', error);
  }
};


// lancer la mis à jour après la modification d'un champ du formulaire 
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

const debouncedSimulateur = debounce(simulateur, 1500);
watch(form, () => {
  debouncedSimulateur();
}, { deep: true });


// Exécutes la fonction au moment où le composant est monté dans le DOM
onMounted(fetchClients);
</script>

<!-- Import du style  -->
<style scoped>
@import '../assets/styles/simulateur-style.css';
</style>

