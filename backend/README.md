
🚀 Application  FastAPI - Backend - Simulio

📁 Structure du projet

- `main.py` : Point d'entrée principal du backend (démarre le serveur FastAPI).
- `src/` :
  - `authentification/` : Fonctions de création et vérification des tokens JWT.
  - `config/` :
    - `database.py` : Gestion de la connexion à la base de données MySQL via SQLAlchemy ( vous devez modifier ici les accès à votre base de données MySQL )
    - `test.py` : Fonctions pour effectuer des calculs liés aux simulations.
  - `controller/` : Logique métier, validation des données reçues, et interface entre les modèles et la base.
  - `models/` : Définitions des classes ORM qui correspondent aux tables de la base de données.
  - `route/` : Définition des endpoints REST (GET, POST, DELETE, PUT), tous sécurisés grâce au système d’authentification dans `auth.py` situé dans `authentification/`.



⚙️ Bibliothèques utilisées

- `fastapi` : Framework web moderne et rapide pour construire des APIs.
- `uvicorn` : Serveur ASGI utilisé pour lancer l’application.
- `sqlalchemy` : ORM pour interagir avec la base de données MySQL.
- `pymysql` : Connecteur MySQL pour Python.
- `python-jose[cryptography]` : Pour créer et vérifier des tokens JWT.
- `passlib[bcrypt]` : Gestion sécurisée des mots de passe.
- `pandas`, `numpy`, `numpy_financial` : Librairies pour calculs et traitements statistiques/financiers.



🛠️ Installation 

### Prérequis

- Python 3.8+ installé,  lien de téléchargement https://www.python.org/downloads/. 
- MySQL installé et configuré (ou un autre serveur compatible MySQL).


✨ Lancement de l'application ✨

###  Lancez ces comandes dans le terminal 

### 1. Cloner le projet

        ```bash
        git clone https://github.com/heriol-valdo/Simulio.git
        cd backend
        ```

### 2. Créer et activer un environnement virtuel 

        ```bash
        python -m venv venv
        # Sous Linux/macOS
        source venv/bin/activate
        # Sous Windows
        venv\Scripts\activate
        ```

### 3. Installer les dépendances Python

        ```bash
        pip update
        ```

        ```bash
        pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] python-dotenv passlib[bcrypt] pandas numpy numpy_financial
        ```


### 4. Lancer le serveur de développement FastAPI

        ```bash
        uvicorn main:app --reload
        ```
### 5.  Exécuter le script SQL contenu dans le fichier dump.sql dans votre base de données MySQL 


- L’API sera accessible par défaut sur [http://localhost:8000]



## 🧩 Fonctionnalités principales pour l’utilisateur

- Authentification : connexion, création de compte avec  gestion de tokens JWT.
- Gestion des clients : création, modification, suppression, recherche.
- Gestion des simulations : création et attribution à un client.
- Consultation des simulations liées à un client précis.




