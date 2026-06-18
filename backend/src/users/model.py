from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
import backend.src.utils.models as models
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from backend.src.core.database import Base


class UserDB(models.IdentityDB):
    """
    Modelo ORM que representa um Usuário (atendente) no ecossistema.

    Gerencia o perfil do operador do sistema, incluindo suas credenciais,
    regras de filtragem por intenção, relacionamento polimórfico de identidades,
    histórico de atendimentos com leads e tabela dedicada de métricas em tempo real.

    Attributes:
        id (int): Chave primária referenciando o ID unificado na tabela Identity.
        email (str): Endereço eletrônico criptograficamente tipado e único do usuário.
        senha (str): Hash de segurança para validação de acesso.
        intencao (str): String parametrizada ditando as intenções aceitas de atendimento.
        clientes (list[LeadDB]): Atalho para lista de leads vinculados por relacionamento M2M.
        associations (list[UserLeadAssociation]): Histórico de conversações com metadados.
        metricas (MetricasLeadInUser): Objeto contendo o score de produtividade consolidado (1:1).
    """

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
    __mapper_args__ = {"polymorphic_identity": "user"}

    def __init__(self, email, senha, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.senha = senha

        self.type = "user"


class MetricasLeadInUser(Base):
    """
    Modelo ORM que guarda dados estatísticos e contadores consolidados de um usuário.

    Alimentado periodicamente ou de forma reativa através de triggers/rotinas analíticas
    do backend para evitar sobrecarga de consultas pesadas de agregação (COUNT/AVG).

    Attributes:
        id (int): Chave primária identificadora do registro.
        user_id (int): Chave estrangeira única apontando para o respectivo UserDB.
        total_leads (int): Quantidade macro de leads operados.
        leads_pendentes (int): Totalizador de interações em estado de pendência.
        leads_abertos (int): Totalizador de interações abertas no chat.
        leads_fechados (int): Totalizador de chamados/interações resolvidas.
        avg_satisfacao (float): Score médio aritmético ponderado por avaliações.
        avg_response_time (int): Tempo de latência média de resposta.
        last_aggregated (datetime): Timestamp registrando o momento exato do cálculo analítico.
        user (UserDB): Objeto reverso de referência ao usuário dono das métricas.
    """

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
