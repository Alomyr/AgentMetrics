from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Substitua pelas suas credenciais reais
# O padrão é: dialect+driver://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123A@localhost:5432/db_cachina"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency para ser usada no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
