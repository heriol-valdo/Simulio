from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


# Table simulations qui sera créée au démarrage de l'API, avec ses relations et contraintes
class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    mensualite = Column(Float, nullable=False)
    prix_bien = Column(Float, nullable=False)
    interets = Column(Float, nullable=False)
    assurance_totale = Column(Float, nullable=False)
    frais_notaire = Column(Float, nullable=False)
    garantie_bancaire = Column(Float, nullable=False)
    salaire_minimum = Column(Float, nullable=False)
    montant_finance = Column(Float, nullable=False)
    travaux = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relations
    client = relationship("Client", back_populates="simulations")
    user = relationship("User", back_populates="simulations")
