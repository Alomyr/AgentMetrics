
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union
from pydantic import ConfigDict
from backend.src.utils.validations import normalize_intencao_value

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
