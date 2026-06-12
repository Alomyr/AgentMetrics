import enum

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional, Union
from backend.model.enum import Categoria, StatusEnum
from pydantic import ConfigDict


def normalize_intencao_value(value):
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
    raise ValueError("intencao deve ser uma string ou lista de strings")


# TRATAMENTO DE ENTRADA DO LEAD
class LeadValidation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    conversa_id: int
    numero_lead: str
    numero_user: str
    categoria: Optional[str] = Categoria.MEDIA
    status: Optional[StatusEnum] = StatusEnum.PENDENTE
    resumo_conversa: Optional[str] = None
    intencao: Optional[Union[str, list[str]]] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None

    @field_validator("intencao", mode="before")
    @classmethod
    def normalize_intencao(cls, value):
        return normalize_intencao_value(value)


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


class intenso(BaseModel):
    intencao: Optional[Union[str, list[str]]] = None
    numero: str

    @field_validator("intencao", mode="before")
    @classmethod
    def normalize_intencao(cls, value):
        return normalize_intencao_value(value)


class login_user(BaseModel):
    email: EmailStr
    senha: str


# TRATAMENTO DE ENTRADA DE PAREAMENTO DE USER E LEAD
class user_lead_association:
    conversa_id: int
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
