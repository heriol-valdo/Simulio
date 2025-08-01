from fastapi.responses import JSONResponse
from src.config.database import SessionLocal
from src.models.ClientModel  import  Client 
from src.models.SimulateurModel  import Simulation
from src.config.test import CalculerMensualité39_bis2_ANCIEN
from datetime import datetime

db = SessionLocal() # Création d'une  session

# Fonction pour exécuter une simulation
def simulateur(data: dict, user: dict):
    required_fields = ["duree", "prixBien", "tauxInteret", "tauxAssurance", "apport", "mois", "annee", "tauxFraisAgence", "tauxFraisNotaire", "travaux", "tauxRevalorisation"]
    missing_fields = [field for field in required_fields if field not in data]


    # Vérifier si un champ est manquant ou vide
    if missing_fields:
        return JSONResponse(
            status_code=400,
            content={"status": False, "message": f"Champs manquants : {', '.join(missing_fields)}", "data": None}
        )

    try:
        # Executer la fonction CalculerMensualité39_bis2_ANCIEN qui se trouve dans le ficher test.py
        result = CalculerMensualité39_bis2_ANCIEN(
            data["duree"],
            data["prixBien"],
            data["tauxInteret"],
            data["tauxAssurance"],
            data["apport"],
            data["mois"],
            data["annee"],
            data["tauxFraisAgence"],
            data["tauxFraisNotaire"],
            data["travaux"],
            data["tauxRevalorisation"]
        )

        # Décomposition du résultat en variables distinctes car result renvoie un tuple
        M, I, A, fraisNotaire_val, garantieBancaire, salaireMinimum, df, fraisAgence2, C2, output2, output3, output4, output13, TRAVAUX = result

        # Renvoyer le message de  succès
        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": "Simulation réussie",
                "data": [
                    {
                        "prixBien": data["prixBien"],
                        "mensualite": M,
                        "interets": I,
                        "assurance_totale": A,
                        "frais_notaire": fraisNotaire_val,
                        "garantie_bancaire": garantieBancaire,
                        "salaire_minimum": salaireMinimum,
                        "tableau_amortissement": df,
                        "frais_agence_calcule": fraisAgence2,
                        "montant_finance": C2,
                        "details_financement": output2,
                        "details_credit": output3,
                        "details_financement": output4,
                        "revente_simulee": output13,
                        "travaux": TRAVAUX,
                    }
                ]
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=505,
            content={"status": False, "message": f"Erreur lors de la simulation : {str(e)}", "data": None}
        )

# Fonction pour  ajouter une simulation à un client 
def simulateurRegister(data: dict, current_user: dict):
    required_fields = [
        "clientId", "mensualite","prixBien",  "frais_notaire", "interets", "assurance_totale",
        "garantie_bancaire", "salaire_minimum", "montant_finance","travaux"
    ]


    # Vérification des champs obligatoires
    for field in required_fields:
        if field not in data:
            return JSONResponse(
                status_code=400,
                content={"status": False, "message": f"Le champ '{field}' est requis", "data": None}
            )

    # Vérification que le client existe et appartient à l'utilisateur actuel
    client = db.query(Client).filter_by(id=data["clientId"], user_id=current_user["id"]).first()
    if not client:
        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "Client introuvable ou non autorisé", "data": None}
        )

    try:
        
        simulation = Simulation(
            mensualite=data["mensualite"],
            prix_bien=data["prixBien"],
            interets=data["interets"],
            assurance_totale=data["assurance_totale"],
            frais_notaire=data["frais_notaire"],
            garantie_bancaire=data["garantie_bancaire"],
            salaire_minimum=data["salaire_minimum"],
            montant_finance=data["montant_finance"],
            travaux=data["travaux"],
            client_id=data["clientId"],
            user_id=current_user["id"],
            created_at=datetime.utcnow()
        )

        db.add(simulation)
        db.commit()
        db.refresh(simulation)

        return JSONResponse(
            status_code=201,
            content={
                "status": True,
                "message": "Simulation enregistrée avec succès",
                "data": {
                    "id": simulation.id,
                    "client_id": simulation.client_id
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"Erreur lors de l'enregistrement : {str(e)}", "data": None}
        )
    
# Fonction pour rechercher les simulations d'un client précis
def simulateurAll(client_id: int, current_user: dict):
    simulateurs = db.query(Simulation).filter_by(client_id=client_id, user_id=current_user["id"]).all()

    # Vérifier si il existe des simulations  pour ce client 
    if not simulateurs:
        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "Aucune simulation trouvée", "data": None}
        )
    
    # Renvoyer le message de  succès si existe des simulations pour ce client
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Simulation récupérée avec succès",
            "data": [
                {
                "id": simulateur.id,
                "prixBien": simulateur.prix_bien,
                "mensualite": simulateur.mensualite,
                "frais_notaire": simulateur.frais_notaire,
                "salaire_minimum": simulateur.salaire_minimum,
                "travaux": simulateur.travaux,
                "created_at": simulateur.created_at.isoformat()
               } for simulateur in simulateurs
            ]

        }
    )