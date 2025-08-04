## Lancement du projet

1. Installer Docker : https://www.docker.com/products/docker-desktop
2. Cloner le repo (git clone https://github.com/heriol-valdo/Simulio.git)
3. Modifier les accès à la base de données dans le fichier docker-compose.yml et dans le fichier database.py ( /backend/config/database.py)
4. Lancer :  `docker-compose down`  ensuite  `docker-compose up --build`
5. Accès :
   - Frontend : http://localhost:5173
   - Backend (API docs) : http://localhost:8001/docs
   - MySQL : port 3306
