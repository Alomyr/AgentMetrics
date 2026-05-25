from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models


class ClienteDB(models.PessoaDB):
    __tablename__ = "clientes"
    id = Column("id", Integer, ForeignKey("usuarios.ID"), primary_key=True)
    admin_id = Column("admin_id", Integer, ForeignKey("admins.ID"))
    admin = relationship(
        "AdminDB",
        back_populates="clientes",
        foreign_keys=[admin_id],
        primaryjoin="ClienteDB.admin_id == AdminDB.id",
    )
    categoria = Column("Categoria", String)
    status = Column("Status", String)
    resumo_conversa = Column(String)
    intencao = Column("Inteção", String)
    data_hora_servico = Column("Time", Date)

    __mapper_args__ = {"polymorphic_identity": "cliente"}

    # def __init__(self, admin_id, categoria, status, resumo, intecao, data, **kwargs):
    #     super().__init__(**kwargs)

    #     self.admin_id = admin_id
    #     self.categoria = categoria
    #     self.status = status
    #     self.resumo_conversa = resumo
    #     self.intencao = intecao
    #     self.data_hora_servico = data

    #     self.type = "cliente"
