from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router.index import router #Importer les routes
from src.config.database import Base, engine # Importer la configuration des tables et l'accès à la base de données


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes adresses à communiquer avec le serveur 
    allow_credentials=True, # autorise l'envoie des informations d'authentification
    allow_methods=["*"],  # autorise toutes les méthodes (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # autorise tous les headers (dont Authorization, Content-Type)
)

# Créer les tables au démarrage de l'api
Base.metadata.create_all(bind=engine)

# Inclure les routes
app.include_router(router)
