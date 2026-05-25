from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class PessoaDB(Base):
    __tablename__ = "pessoas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    numero = Column(String)
    # A coluna 'type' define se é um 'admin' ou 'cliente'
    type = Column(String) 
    
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": type,
    }

class AdminDB(PessoaDB):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("pessoas.id"), primary_key=True)
    email = Column(String, unique=True)
    senha = Column(String)
    
    __mapper_args__ = {"polymorphic_identity": "admin"}

class ClienteDB(PessoaDB):
    __tablename__ = "clientes"
    id = Column(Integer, ForeignKey("pessoas.id"), primary_key=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    admin = relationship("AdminDB", back_populates="clientes")
    categoria = Column(String)
    status = Column(String)
    resumo_conversa = Column(String)
    intencao = Column(String)
    data_hora_servico = Column(Date)
    
    
    __mapper_args__ = {"polymorphic_identity": "cliente"}


