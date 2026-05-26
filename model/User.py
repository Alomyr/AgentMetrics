from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import model.models as models


class UserDB(models.IdentityDB):
    __tablename__ = "Users"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    email = Column("Email", String, unique=True, nullable=False)
    senha = Column("Senha", String, nullable=False)
    clientes = relationship(
        "LeadDB",
        secondary=models.user_lead_association,
        back_populates="users",
    )

    __mapper_args__ = {"polymorphic_identity": "user"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha  # colocar logica de criptografia

        self.type = "user"
