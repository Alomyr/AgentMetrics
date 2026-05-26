from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models
from model.enum import StatusEnum
from sqlalchemy_utils.types import ChoiceType


class LeadDB(models.IdentityDB):
    __tablename__ = "Leads"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("Users.ID"))
    user = relationship(
        "UserDB",
        back_populates="clientes",
        foreign_keys=[user_id],
        primaryjoin="UserDB.id == LeadDB.user_id",
    )
    categoria = Column("Categoria", String)
    status = Column("Status", ChoiceType(StatusEnum, impl=String()))
    resumo_conversa = Column(String)
    intencao = Column("Intencao", String)
    data_hora_servico = Column("DataHoraServico", Date)

    __mapper_args__ = {"polymorphic_identity": "lead"}
