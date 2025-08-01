from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

# Table clients qui sera créée au démarrage de l'API, avec ses relations et contraintes
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    number = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relations
    user = relationship("User", back_populates="clients")
    simulations = relationship("Simulation", back_populates="client", cascade="all, delete")

    

