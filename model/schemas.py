from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, List
from model.enum import StatusEnum


class Creat_new_user(BaseModel):
    name: str
    numero: str
    email: str
    senha: str


class LeadsCreate(BaseModel):
    name: str
    numero: str
    user_ids: Optional[List[int]] = None  # IDs dos usuários associados ao lead


class user_lead_association:
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    stisfacao: int


class login_root(BaseModel):
    login: str
    senha: str


class login_user(BaseModel):
    email: str
    senha: str


class lead_is_exist_number(BaseModel):
    name: str
    numero: str
    user_ids: Optional[List[int]] = None
