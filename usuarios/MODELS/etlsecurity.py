import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import bcrypt
from jose import jwt, JWTError

import usuarios.MODELS.etlexceptions as etlException

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# Dos metodos que tienen que ver con contrasenas
def hash_password(password: str) -> str:
    # Convierte la contrasena en hash al crear un usuario
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara la contrasena en texto plano contra el hash guardado
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# En FastAPI el token lo inyectaba HTTPBearer con Depends().
# En Django el equivalente es leer el header a mano desde el request.
def get_token_from_request(request) -> str:
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise etlException.BusinessError(1008, "Falta el token de autenticación", 401)

    return token

def get_current_user(request) -> str:
    token = get_token_from_request(request)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise etlException.BusinessError(1006, "Token inválido", 401)

        return username
    except JWTError:
        raise etlException.BusinessError(1007, "Token inválido o expirado", 401)

def get_current_user_from_refresh_token(request) -> str:
    token = get_token_from_request(request)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise etlException.BusinessError(1006, "Token inválido", 401)

        return username
    except JWTError:
        raise etlException.BusinessError(1007, "Token inválido o expirado", 401)
