# core/security.py
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from backend.src.core.database import get_db
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.src.users.model import UserDB
from backend.src.core.config import SECRET_KEY, ALGORITHM

load_dotenv()
SECURITY_KEY = os.getenv("SECURITY_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/login")


def verificar_token(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
    user = db.query(UserDB).filter(UserDB.id == id_user).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não existe")
    return user
