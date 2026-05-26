from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Substitua pelas suas credenciais reais quando fizer o deployd
# O padrão é: dialect+driver://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/cachina_db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para ser usada no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class IdentityDB(Base):
    __tablename__ = "Identity"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Nome", String, nullable=False)
    numero = Column("Numero", String, nullable=False)
    # A coluna 'type' define se é um 'admin' ou 'cliente'
    type = Column("Tipo", String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "identity",
        "polymorphic_on": type,
    }
