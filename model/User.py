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
        secondary=models.UserLeadAssociation.__table__,
        back_populates="users",
    )
    #Empresa nome
    #um para muitos nova tabela
    # association objects (to store extra metadata about the relation)
    associations = relationship(
        "UserLeadAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )
#documentos pos um dia apagar => modelo de documento
    __mapper_args__ = {"polymorphic_identity": "user"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha  # colocar logica de criptografia

        self.type = "user"
