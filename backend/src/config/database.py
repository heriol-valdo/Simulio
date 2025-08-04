from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
import sys

# Variables d'environnement avec valeurs par défaut
import os

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "dump")
DB_USER = os.getenv("DB_USER", "heriol")
DB_PASSWORD = os.getenv("DB_PASSWORD", "monSuperMotDePasse123!")

print(f"[DEBUG] Connexion à MySQL sur {DB_HOST}:{DB_PORT} avec utilisateur {DB_USER}")

DATABASE_URL = "mysql+pymysql://heriol:monSuperMotDePasse123!@mysql:3307/dump"


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
