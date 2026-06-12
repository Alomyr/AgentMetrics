import enum

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional, Union
from backend.src.utils.enum import Categoria, StatusEnum
from pydantic import ConfigDict


# TRATAMENTO DE ENTRADA DE PAREAMENTO DE USER E LEAD
class user_lead_association:
    conversa_id: int
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None


