# core/security.py
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from backend.src.core.database import get_db
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.src.users.model import UserDB
from backend.src.core.config import SECRET_KEY, ALGORITHM
# Inicializa o contexto para hashing e verificação de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define o esquema OAuth2 para extração automática do token JWT do cabeçalho HTTP
oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/login-forms")


def get_password_hash(password: str) -> str:
    """
    Gera o hash criptográfico seguro de uma senha em texto plano usando Bcrypt.

    Args:
        password (str): Senha em formato de texto limpo enviada pelo cliente.

    Returns:
        str: O hash Bcrypt resultante pronto para armazenamento seguro.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a um hash Bcrypt existente.

    Args:
        plain_password (str): Senha em texto limpo enviada para validação.
        hashed_password (str): O hash seguro armazenado no banco de dados.

    Returns:
        bool: True se a senha for válida/correta, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def verificar_token(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> UserDB:
    """
    Valida a assinatura do token JWT e retorna o usuário correspondente se ativo.

    Utilizado como dependência de rotas protegidas que exigem autenticação.

    Args:
        token (str): O token Bearer JWT interceptado na requisição HTTP.
        db (Session): Sessão ativa do banco de dados injetada automaticamente.

    Raises:
        HTTPException: Erro 401 caso o token seja inválido ou esteja expirado.
        HTTPException: Erro 400 caso o usuário dono do token não seja localizado.

    Returns:
        UserDB: O objeto do usuário autenticado no banco de dados.
    """
    try:
        # Decodifica e valida criptograficamente a assinatura digital do token
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
        
    # Busca a existência do usuário no banco com base no ID extraído do payload
    user = db.query(UserDB).filter(UserDB.id == id_user).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não existe")
        
    return user