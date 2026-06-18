from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.src.core.config import SQLALCHEMY_DATABASE_URL

# Criação da classe base para os modelos ORM
Base = declarative_base()

# Inicialização do motor de conexão do banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configuração da fábrica de sessões locais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Gerencia o ciclo de vida de uma sessão de banco de dados.

    Criado para ser injetado como dependência nas rotas do FastAPI. Garante que
    uma nova sessão seja aberta por requisição e estritamente fechada ao término dela.

    Yields:
        Iterator[Session]: Uma instância ativa de sessão de banco de dados (SessionLocal).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()