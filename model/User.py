from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models
from model.Leads import LeadDB


class UserDB(models.IdentityDB):
    __tablename__ = "Users"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    email = Column("Email", String, unique=True, nullable=False)
    senha = Column("Senha", String, nullable=False)
    clientes = relationship(
        "LeadDB",
        back_populates="user",
        foreign_keys="[LeadDB.user_id]",
        primaryjoin="UserDB.id == LeadDB.user_id",
    )

    __mapper_args__ = {"polymorphic_identity": "user"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha  # colocar logica de criptografia

        self.type = "user"
