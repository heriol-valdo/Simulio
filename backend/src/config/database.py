from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
import sys

# Variables d'environnement avec valeurs par défaut
import os

 # heriol  : Remplacez ceci par le nom de votre utilisateur, différent de l'utilisateur root par défaut. 
 # monSuperMotDePasse123! : Remplacez ceci par le mot de passe de votre utilisateur, différent du mot de passe par défaut de l'utilisateur root.

DATABASE_URL = "mysql+pymysql://heriol:monSuperMotDePasse123!@mysql:3306/dump"


def create_database_connection(max_retries=10, retry_delay=5):
    for attempt in range(max_retries):
        try:
            print(f"Connexion MySQL essai {attempt + 1}...")
            engine = create_engine(DATABASE_URL, echo=True)
            with engine.connect() as connection:
                print("✓ Connexion réussie à MySQL")
                return engine
        except Exception as e:
            print(f"✗ Échec: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                sys.exit("Erreur critique: impossible de se connecter à MySQL")

engine = create_database_connection()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
