from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

load_dotenv(".env")
KEY :str = os.getenv("SECRET_KEY")
ALGO :str = os.getenv("ALGORITHM")
# TOKEN_EXPIRE_MINUTES  = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
# SECRET_KEY = "8b54ead9cc95dcd524805bd175d549707314c8bd7020c33782c9b4d01592dfd1"
# ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGO)
    return encoded_jwt