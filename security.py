from pwdlib import PasswordHash
import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")


password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str,stored_hash: str):
    return password_hash.verify(password, stored_hash)


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

def decode_access_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    return payload
