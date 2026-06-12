from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import backend.model.models as models
from backend.model.enum import StatusEnum


class LeadDB(models.IdentityDB):
    __tablename__ = "Leads"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    users = relationship(
        "UserDB",
        secondary=models.UserLeadAssociation.__table__,
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
