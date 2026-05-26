from pydantic import BaseModel
from datetime import date
from typing import Optional
from model.enum import StatusEnum


class Creat_new_user(BaseModel):
    name: str
    numero: str
    email: str
    senha: str


class LeadsCreate(BaseModel):
    name: str
    numero: str
    user_id: int  # Incluído aqui para vir no JSON
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
