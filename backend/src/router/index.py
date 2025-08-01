from fastapi import APIRouter, Depends
from src.authentication.auth import verify_token
from src.controllers.UserController import userRegister, userLogin, userProfile
from src.controllers.ClientController import clientRegister, clientAll, clientOne, clientUpdate, clientDelete
from src.controllers.SimulateurController import simulateur, simulateurRegister, simulateurAll

router = APIRouter()

# route des  utilisateurs

# route pour enregistrement d'un utilisateur  
@router.post("/userRegister")
def userRegisterRoute(data: dict):
    return userRegister(data)

# route de connexion d'un utilisateur
@router.post("/userLogin")
def userLoginRoute(data: dict):
    return userLogin(data)

# route de récupèration des indormations d'un utilisateur  
@router.get("/userProfile")
def userProfileRoute(user: dict = Depends(verify_token)):
    return userProfile(user)



#route des clients clients

#route pour  ajouter un client
@router.post("/clientRegister")
def clientRegisterRoute(data: dict, user: dict = Depends(verify_token)):
    return clientRegister(data, user)

#route pour récupèrer les clients 
@router.get("/clientAll")
def clientAllRoute(user: dict = Depends(verify_token)):
    return clientAll(user)

#route pour  récupèrer les informations d'un client précis
@router.get("/clientOne/{client_id}")
def clientOneRoute(client_id: int, user: dict = Depends(verify_token)):
    return clientOne(client_id, user)

#route pour modifier un client
@router.put("/clientUpdate/{client_id}")
def clientUpdateRoute(client_id: int, data: dict, user: dict = Depends(verify_token)):
    return clientUpdate(client_id, data, user)

#route pour  supprimer un client
@router.delete("/clientDelete/{client_id}")
def clientDeleteRoute(client_id: int, user: dict = Depends(verify_token)):
    return clientDelete(client_id, user)


# route des simulations

#route pour exécuter une simulation
@router.post("/simulateur")
def simulateurRoute(data: dict, user: dict = Depends(verify_token)):
    return simulateur(data,user)

#route pour  ajouter une simulation à un client 
@router.post("/simulateurRegister")
def simulateurRegisterRoute(data: dict, user: dict = Depends(verify_token)):
    return simulateurRegister(data,user)

#route pour rechercher les simulations d'un client précis
@router.get("/simulateurAll/{client_id}")
def simulateurAllRoute(client_id: int, user: dict = Depends(verify_token)):
    return simulateurAll(client_id,user)

