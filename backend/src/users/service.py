from dns import query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.core.security import (
    get_password_hash,
    verify_password,
    verificar_token,
)
from backend.src.leads.model import LeadDB
from backend.src.utils.schemas import user_lead_association
from backend.src.utils.validations import get_record, result_check, insert_db
from backend.src.users.model import UserDB
from backend.src.users.schemas import Creat_new_user, login_user, intenso
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from backend.src.core.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.leads.model import UserLeadAssociation


def token(
    user_id: int, duracao: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    """
    Gera um token criptográfico JWT assinado para o usuário.

    Args:
        user_id (int): Identificador único do usuário que será inserido no claim 'sub'.
        duracao (timedelta): Tempo de validade do token. Padrão: ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: String codificada do token JWT.
    """
    data_expiracao = datetime.now(timezone.utc) + duracao
    dic_info = {"sub": str(user_id), "exp": data_expiracao}
    return jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)


def serialize_intencao(value) -> str | None:
    """
    Sanitiza e normaliza o campo intenção para gravação consistente no banco de dados.

    Converte formatos mistos (listas ou strings isoladas) em uma única string
    separada por vírgulas e sem espaços residuais.
    """
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    if isinstance(value, list):
        normalized = [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]
        return ",".join(normalized) if normalized else None
    raise HTTPException(
        status_code=400, detail="intencao deve ser uma string ou lista de strings"
    )
