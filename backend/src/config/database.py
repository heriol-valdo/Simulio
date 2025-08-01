from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Adresse pour se connecter à la base de données MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost/dump"

engine = create_engine(DATABASE_URL) # Crée la connexion à la base de données
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # générateur de sessions pour faire des actions 
Base = declarative_base() # Crée une base pour définir les tables

