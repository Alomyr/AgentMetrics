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
