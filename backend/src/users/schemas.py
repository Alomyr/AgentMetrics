from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union
from pydantic import ConfigDict
from backend.src.utils.validations import normalize_intencao_value


class Creat_new_user(BaseModel):
    """
    Schema Pydantic para validação de dados no fluxo de criação de um usuário.

    Attributes:
        name (str): Nome completo do atendente.
        numero (str): Número identificador ou telefone exclusivo do atendente.
        email (EmailStr): Endereço de e-mail verificado do usuário.
        senha (str): Senha em texto plano a ser convertida em hash.
    """
    model_config = ConfigDict(from_attributes=True)
    name: str
    numero: str
    email: EmailStr
    senha: str


class edit_user(BaseModel):
    """
    Schema Pydantic para atualização cadastral do perfil do usuário.

    Attributes:
        numero (str, optional): Novo número identificador do usuário.
        nome (str, optional): Novo nome completo do usuário.
        email (EmailStr, optional): Novo e-mail validado.
        nova_senha (str): Nova senha em formato limpo exigida para concluir a alteração.
    """
    numero: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    nova_senha: str


class intenso(BaseModel):
    """
    Schema Pydantic para configuração e atualização das intenções de um atendente.

    Attributes:
        intencao (str | list[str], optional): Definição de tags/intenções de atendimento.
    """
    intencao: Optional[Union[str, list[str]]] = None

    @field_validator("intencao", mode="before")
    @classmethod
    def normalize_intencao(cls, value):
        """
        Normaliza os dados do campo de intenção antes da validação de tipo do Pydantic.
        """
        return normalize_intencao_value(value)


class login_user(BaseModel):
    """
    Schema Pydantic para validação das credenciais de autenticação baseadas em JSON.

    Attributes:
        email (EmailStr): E-mail cadastrado do usuário que solicita acesso.
        senha (str): Senha em formato de texto plano fornecida no ato do login.
    """
    email: EmailStr
    senha: str