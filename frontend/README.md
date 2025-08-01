 🚀 Application Vue.js - Frontend - Simulio

 📁 Structure du projet

- `main.js` : Point d’entrée principal de l’application Vue.js.
- `App.vue` : Composant racine qui structure l’application.
- `src/`
  - `assets/` : Images, styles et ressources statiques.
  - `components/` : Composants réutilisables (ex: `ShowToast`).
  - `config/` : Configuration (`axios`) pour les requêtes vers le backend.
  - `models/` : Entités de l’application et gestion des requêtes via `axios`.
  - `route/` : Gestion des routes, avec système de vérification d’accès.
  - `templates/` : Composants de la structure générale (header, navbar, footer).
  - `views/` : Vues principales de l’application.



⚙️ Actions possibles pour un utilisateur

- Se connecter / créer un compte
- Se déconnecter
- Créer, modifier, supprimer et rechercher un client
- Faire une simulation
- Attribuer une simulation à un client
- Voir les simulations d’un client précis



📦 Installation 

### Prérequis

- Node.js installé,  lien de téléchargement https://nodejs.org/en/
- npm https://www.npmjs.com/



✨ Lancement de l'application ✨

###  Lancez ces comandes dans le terminal 

### 1. Cloner le projet

    ```bash
        git clone https://github.com/heriol-valdo/Simulio.git
        cd frontend
    ```

### 2. Installer les dépendances ou mis à jour 

        ```bash
        npm install
        npm update
        ```

### 3. Lancer l'application en mode développement

        ```bash
        npm run dev
        ```

- L'application sera accessible par défaut sur [http://localhost:5173]



📋 Technologies utilisées

- Vue.js 3
- Vue Router
- Axios pour les requêtes HTTP
- Lodash & Lodash.debounce pour l’optimisation
- Vite 



