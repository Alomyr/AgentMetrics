from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, Union
from backend.src.utils.enum import Categoria, StatusEnum
from pydantic import ConfigDict
from backend.src.utils.validations import normalize_intencao_value


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
