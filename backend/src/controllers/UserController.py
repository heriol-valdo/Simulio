from fastapi.responses import JSONResponse
from src.config.database import SessionLocal
from src.models.UserModel import User
from src.authentication.auth import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Configurer un gestionnaire de hachage de mots de passe
db = SessionLocal() # Création d'une  session

# Fonction pour enregistrement d'un utilisateur  
def userRegister(data: dict):
    required_fields = ["firstname", "lastname", "address", "email", "password"]


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
                content={
                    "status": False,
                    "message": f"Le champ '{field}' est requis",
                    "data": None
                }
            )

    # Vérification de l’unicité de l’email
    if db.query(User).filter_by(email=data["email"]).first():
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Email déjà utilisé",
                "data": None
            }
        )

    # Hasher le  mot de passe
    hashed_password = pwd_context.hash(data["password"])
    user = User(
        firstname=data["firstname"],
        lastname=data["lastname"],
        address=data["address"],
        email=data["email"],
        password=hashed_password
    )

    # Enregistrement en base
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=201,
        content={
            "status": True,
            "message": "Utilisateur enregistré avec succès",
            "data": {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "address": user.address
            }
        }
    )

# Fonction de connexion d'un utilisateur
def userLogin(data: dict):
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    # Vérification des champs vides
    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "L'email et le mot de passe sont requis",
                "data": None
            }
        )

    # Vérification des identifiants
    user = db.query(User).filter_by(email=email).first()
    if not user or not pwd_context.verify(password, user.password):
        return JSONResponse(
            status_code=401,
            content={
                "status": False,
                "message": "Identifiants invalides",
                "data": None
            }
        )

    # Génération du token
    token = create_access_token({"sub": user.email, "id": user.id })
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Connexion réussie",
            "data": {
                "access_token": token,
                "token_type": "bearer"
            }
        }
    )

# Fonction de de récupèration des indormations d'un utilisateur 
def userProfile(current_user: dict):
    user = db.query(User).filter_by(email=current_user["sub"]).first()

    # Vérifier si l'utilisateur existe
    if not user:
        return JSONResponse(
            status_code=404,
            content={
                "status": False,
                "message": "Utilisateur non trouvé",
                "data": None
            }
        )

    # Renvoyer les informations de l'utilisateur
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Profil récupéré avec succès",
            "data": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "address": user.address
            }
        }
    )
