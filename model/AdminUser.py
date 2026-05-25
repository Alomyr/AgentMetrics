from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models


class AdminDB(models.PessoaDB):
    __tablename__ = "admins"
    id = Column("ID", Integer, ForeignKey("usuarios.ID"), primary_key=True)
    email = Column("Email", String, unique=True, nullable=False)
    senha = Column("Senha", String, nullable=False)
    clientes = relationship(
        "ClienteDB",
        back_populates="admin",
        foreign_keys="[ClienteDB.admin_id]",
        primaryjoin="AdminDB.id == ClienteDB.admin_id",
    )

    __mapper_args__ = {"polymorphic_identity": "admin"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha  # colocar logica de criptografia

        self.type = "admin"
