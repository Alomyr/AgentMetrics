from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
import backend.src.utils.models as models
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


class UserDB(models.IdentityDB):
    __tablename__ = "Users"
    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)
    email = Column("Email", EmailType, unique=True, nullable=False)
    senha = Column("Senha", String, nullable=False)
    intencao = Column(
        "intensao",
        String,
    )
    clientes = relationship(
        "LeadDB",
        secondary="user_lead_association",
        back_populates="users",
    )
    # Empresa nome
    # muito para muitos
    # association objects (to store extra metadata about the relation)
    associations = relationship(
        "UserLeadAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    metricas = relationship(
        "MetricasLeadInUser",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    # documentos pos um dia apagar => modelo de documento
    __mapper_args__ = {"polymorphic_identity": "user"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha  # colocar logica de criptografia

        self.type = "user"


class MetricasLeadInUser(Base):
    __tablename__ = "metricas_lead_in_user"

    id = Column("ID", Integer, primary_key=True, index=True)
    user_id = Column(
        "user_id", Integer, ForeignKey("Users.ID"), unique=True, nullable=False
    )

    total_leads = Column("total_leads", Integer, default=0)
    leads_pendentes = Column("leads_pendentes", Integer, default=0)
    leads_abertos = Column("leads_abertos", Integer, default=0)
    leads_fechados = Column("leads_fechados", Integer, default=0)
    avg_satisfacao = Column("avg_satisfacao", Float)
    avg_response_time = Column("avg_response_time", Integer)
    last_aggregated = Column("last_aggregated", DateTime)

    # relacionamento para acessar o usuário dono dessas métricas
    user = relationship("UserDB", back_populates="metricas")
