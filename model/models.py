from sqlalchemy import Column, Integer, String, Date, ForeignKey, column
from .database import Base


class IdentityDB(Base):
    __tablename__ = "Identity"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    numero = Column("Numero", String, unique=True, nullable=False)
    # A coluna 'type' define se é um 'admin' ou 'cliente'
    type = Column("Tipo", String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "identity",
        "polymorphic_on": type,
    }


class Admin(Base):
    __tablename__ = "ADMINISTRADORES"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    login = Column("Root", String, nullable=False, unique=True)
    senha = Column("Senha", String, nullable=False)
