from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models
from model.enum import StatusEnum


class LeadDB(models.IdentityDB):
    __tablename__ = "Leads"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    users = relationship(
        "UserDB",
        secondary=models.user_lead_association,
        back_populates="clientes",
    )
    categoria = Column("Categoria", String)
    status = Column("Status", String)
    resumo_conversa = Column(String)
    intencao = Column("Intencao", String)
    data_hora_servico = Column("DataHoraServico", Date)
    stisfacao = Column("Avaliação da conversa", Integer)

    __mapper_args__ = {"polymorphic_identity": "lead"}


# NOTE: falta fazer o sistema para criar os registros de conversas dos lead com varios users
