from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base

# Table users qui sera créée au démarrage de l'API, avec ses relations et contraintes
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    address = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))

    # Relations
    clients = relationship("Client", back_populates="user")
    simulations = relationship("Simulation", back_populates="user", cascade="all, delete")

