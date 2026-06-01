from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from model.enum import StatusEnum


# TRATAMENTO DE ENTRADA DO LEAD
class LeadValidation(BaseModel):
    name: Optional[str] = None
    numero_lead: str
    numero_user: str


# TRATAMENTO DE ENTRADA DO USER
class Creat_new_user(BaseModel):
    name: str
    numero: str
    email: str
    senha: str


# TRATAMENTO DE ENTRADA DO ROOT
class login_root(BaseModel):
    login: str
    senha: str


class login_user(BaseModel):
    email: str
    senha: str


# TRATAMENTO DE ENTRADA DE PAREAMENTO DE USER E LEAD
class user_lead_association:
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    stisfacao: int
