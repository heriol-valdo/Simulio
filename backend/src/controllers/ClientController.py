from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.config.database import SessionLocal
from src.models.ClientModel import Client

db = SessionLocal() # Création d'une  session


# Fonction pour  ajouter un client
def clientRegister(data: dict, current_user: dict):
    required_fields = ["firstname", "lastname", "address", "number", "email"]

    # Vérifier la taille de l'email  
    if len(data["email"]) > 50:
         return JSONResponse(
            status_code=400,
            content={"status": False, "message": "L'email ne doit pas dépasser 50 caractères", "data": None}
    )
    
    # Vérifier si un champ est manquant ou vide
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return JSONResponse(
                status_code=400,
                content={"status": False, "message": f"Le champ '{field}' est requis", "data": None}
            )

    # Vérifier unicité email parmi les clients de cet utilisateur uniquement
    if db.query(Client).filter_by(email=data["email"], user_id=current_user["id"]).first():
        return JSONResponse(
            status_code=400,
            content={"status": False, "message": "Email déjà utilisé pour un autre client", "data": None}
        )

    client = Client(
        firstname=data["firstname"],
        lastname=data["lastname"],
        address=data["address"],
        number=data["number"],
        email=data["email"],
        user_id=current_user["id"]
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return JSONResponse(
        status_code=201,
        content={
            "status": True,
            "message": "Client ajouté avec succès",
            "data": {
                "id": client.id,
                "firstname": client.firstname,
                "lastname": client.lastname,
                "email": client.email,
                "address": client.address,
                "number": client.number
            }
        }
    )


# Fonction pour récupèrer les clients 
def clientAll(current_user: dict):
    clients = db.query(Client).filter_by(user_id=current_user["id"]).all()

    # Renvoyer le message de  succès
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Liste des clients récupérée",
            "data": [
                {
                    "id": c.id,
                    "firstname": c.firstname,
                    "lastname": c.lastname,
                    "email": c.email,
                    "address": c.address,
                    "number": c.number
                } for c in clients
            ]
        }
    )


# Fonction pour  récupèrer les informations d'un client précis
def clientOne(client_id: int, current_user: dict):
    client = db.query(Client).filter_by(id=client_id, user_id=current_user["id"]).first()

      # Vérifier si le client existe
    if not client:
        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "Client non trouvé", "data": None}
        )

    # Renvoyer le message de  succès
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Client récupéré avec succès",
            "data": {
                "id": client.id,
                "firstname": client.firstname,
                "lastname": client.lastname,
                "email": client.email,
                "address": client.address,
                "number": client.number
            }
        }
    )


# Fonction pour modifier un client
def clientUpdate(client_id: int, data: dict, current_user: dict):
    client = db.query(Client).filter_by(id=client_id, user_id=current_user["id"]).first()
    
    # Vérifier la taille de l'email
    if "email" in data and len(data["email"]) > 50:
       return JSONResponse(
        status_code=400,
        content={"status": False, "message": "Email trop long (max. 50 caractères)", "data": None}
    )


    # Vérifier si l'id client est présent
    if not client_id:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "L'identifiant du client est requis",
                "data": None
            }
        )
    
    # Vérifier si le  client est existe
    if not client:
        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "Client non trouvé", "data": None}
        )

    # Vérifier si un autre client utilise déjà le même email
    if "email" in data:
        existing = db.query(Client).filter(Client.email == data["email"], Client.id != client.id).first()
        if existing:
            return JSONResponse(
                status_code=400,
                content={"status": False, "message": "Cet email est déjà utilisé par un autre client", "data": None}
            )

    # Mise à jour des champs autorisés
    for key in ["firstname", "lastname", "address", "number", "email"]:
        if key in data:
            setattr(client, key, data[key])

    try:
        db.commit()
        db.refresh(client)
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"status": False, "message": "Erreur lors de la mise à jour du client (doublon ?)", "data": None}
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Client mis à jour avec succès",
            "data": {
                "id": client.id,
                "firstname": client.firstname,
                "lastname": client.lastname,
                "email": client.email,
                "address": client.address,
                "number": client.number
            }
        }
    )


# Fonction  pour  supprimer un client
def clientDelete(client_id: int, current_user: dict):
    client = db.query(Client).filter_by(id=client_id, user_id=current_user["id"]).first()

    # Vérifier si l'id client est présent
    if not client_id:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "L'identifiant du client est requis",
                "data": None
            }
        )
   
    # Vérifier si le client existe
    if not client:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "Client non trouvé", "data": None}
        )

    db.delete(client)
    db.commit()

    # Renvoyer le message de  succès
    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "Client supprimé avec succès", "data": None}
    )
