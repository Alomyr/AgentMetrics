from dotenv import load_dotenv
import os

# Carrega variáveis do .env imediatamente ao importar este módulo
load_dotenv()

# Configurações da aplicação
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
SECRET_KEY = os.getenv("SECRET_KEY", os.getenv("SECURITY_KEY"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
