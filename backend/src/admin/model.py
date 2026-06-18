from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from backend.src.core.database import Base


class Admin(Base):
    """_summary_
    Representa a entidade de um Administrador no sistema.

    Mapeia os dados dos usuários administradores para a tabela 'ADMINISTRADORES',
    armazenando credenciais de login e informações básicas de identificação.

    Attributes:
        id (int): Chave primária e identificador único do administrador.
        name (str): Nome completo do administrador.
        login (str): Nome de usuário único utilizado para o acesso.
        senha (str): Hash da senha de autenticação.
    """

    __tablename__ = "ADMINISTRADORES"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    login = Column("Login", String, nullable=False, unique=True)
    senha = Column("Senha", String, nullable=False)
