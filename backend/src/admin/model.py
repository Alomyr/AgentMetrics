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


class Admin(Base):
    __tablename__ = "ADMINISTRADORES"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    login = Column("Login", String, nullable=False, unique=True)
    senha = Column("Senha", String, nullable=False)

