from sqlalchemy import Column, Integer, String
from ..core.database import Base


class IdentityDB(Base):
    """
    Modelo ORM Base que representa uma Identidade unificada no sistema.

    Atua como a tabela pai no padrão de herança polimórfica (Joined Table Inheritance).
    Agrupa informações compartilhadas obrigatórias entre múltiplos perfis de agentes,
    como Leads e Usuários.

    Attributes:
        id (int): Chave primária universal e indexada para herança relacional.
        name (str): Nome cadastrado da entidade (User ou Lead).
        numero (str): Número identificador único global de comunicação.
        type (str): Coluna discriminadora mapeada para resolver o polimorfismo do ORM.
    """

    __tablename__ = "Identity"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    numero = Column("Numero", String, unique=True, nullable=False)
    type = Column("Tipo", String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "identity",
        "polymorphic_on": type,
    }
