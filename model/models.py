from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    column,
    Table,
    UniqueConstraint,
)
from .database import Base

user_lead_association = Table(
    "user_leads",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("Users.ID"), primary_key=True),
    Column("lead_id", Integer, ForeignKey("Leads.ID"), primary_key=True),
    UniqueConstraint("user_id", "lead_id", name="uix_user_lead"),
)


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
