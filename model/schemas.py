from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from model.enum import StatusEnum
from pydantic import ConfigDict


# TRATAMENTO DE ENTRADA DO LEAD
class LeadValidation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    numero_lead: str
    numero_user: str
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None


# TRATAMENTO DE ENTRADA DO USER
class Creat_new_user(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    numero: str
    email: EmailStr
    senha: str


class edit_user(BaseModel):
    numero: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    nova_senha: str


class login_user(BaseModel):
    email: EmailStr
    senha: str


# TRATAMENTO DE ENTRADA DE PAREAMENTO DE USER E LEAD
class user_lead_association:
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None


# TRATAMENTO DE ENTRADA DO ROOT
class login_root(BaseModel):
    login: str
    senha: str
