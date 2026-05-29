from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base


class Admin(Base):
    __tablename__ = "ADMINISTRADORES"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    login = Column("Login", String, nullable=False, unique=True)
    senha = Column("Senha", String, nullable=False)


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


class UserLeadAssociation(Base):
    __tablename__ = "user_lead_association"

    user_id = Column("user_id", Integer, ForeignKey("Users.ID"), primary_key=True)
    lead_id = Column("lead_id", Integer, ForeignKey("Leads.ID"), primary_key=True)
    data_hora_servico = Column("data_hora_servico", Date)
    status = Column("status", String)
    categoria = Column("categoria", String)
    intencao = Column("intencao", String)
    satisfacao = Column("satisfacao", Integer)
    resumo_conversa = Column("resumo_conversa", String)

    # relationships to access parent objects from the association
    user = relationship("UserDB", back_populates="associations")
    lead = relationship("LeadDB", back_populates="associations")
