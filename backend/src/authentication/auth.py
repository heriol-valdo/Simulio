from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "ïOÖbÈ3~_Äijb¥d-ýÇ£Hf¿@xyLcP÷@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Variable qui permet de definir  un moyen d’extraire un token d’accès OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Fonction de création d'un token à base de la clé secrète et de l'algorithme
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction de vérification de la validité  d'un token
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")

        if exp is None or datetime.fromtimestamp(exp) < datetime.utcnow():
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": False,
                    "message": "Token expiré",
                    "data": None
                }
            )

        return payload

    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "Token invalide",
                "data": None
            }
        )
