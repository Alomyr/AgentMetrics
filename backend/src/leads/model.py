from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import backend.src.utils.models as models
from backend.src.utils.enum import StatusEnum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from backend.src.core.database import Base


class LeadDB(models.IdentityDB):
    __tablename__ = "Leads"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    users = relationship(
        "UserDB",
        secondary="user_lead_association",
        back_populates="clientes",
    )
    # association objects (to store extra metadata about the relation)
    associations = relationship(
        "UserLeadAssociation",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    __mapper_args__ = {"polymorphic_identity": "lead"}


# NOTE: falta fazer o sistema para criar os registros de conversas dos lead com varios users


class UserLeadAssociation(Base):
    __tablename__ = "user_lead_association"

    conversa_id = Column("ID da conversao", Integer, primary_key=True)
    lead_id = Column("lead_id", Integer, ForeignKey("Leads.ID"))
    user_id = Column("user_id", Integer, ForeignKey("Users.ID"))

    lead_name = Column("lead_name", String)
    lead_number = Column("lead_number", String)

    status = Column("status", String)
    categoria = Column("categoria", String)
    intencao = Column("intencao", String)
    satisfacao = Column("satisfacao", Integer)
    resumo_conversa = Column("resumo_conversa", String)
    data_hora_servico = Column("data_hora_servico", Date)

    # relationships to access parent objects from the association
    user = relationship("UserDB", back_populates="associations")
    lead = relationship("LeadDB", back_populates="associations")
