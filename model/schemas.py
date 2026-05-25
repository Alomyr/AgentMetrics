from pydantic import BaseModel
from datetime import date
from typing import Optional
from model.enum import StatusEnum


class AdminCreate(BaseModel):
    name: str
    numero: str
    email: str
    senha: str


class ClienteCreate(BaseModel):
    name: str
    numero: str
    admin_id: int  # Incluído aqui para vir no JSON
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
