from dotenv import load_dotenv
import os


load_dotenv()

"""
Módulo de Configuração Global e Carregamento de Ambiente.

Este script é responsável por inicializar as variáveis de ambiente utilizando 
a biblioteca `python-dotenv`. Ele centraliza os parâmetros de segurança do JWT 
(JSON Web Tokens) e as credenciais de conexão com o banco de dados relacional.

Attributes:
    ACCESS_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração do token de acesso.
    SECRET_KEY (str): Chave secreta de criptografia para assinatura do token.
    ALGORITHM (str): Algoritmo de hash utilizado (padrão HMAC-SHA256).
    SQLALCHEMY_DATABASE_URL (str): String de conexão da Session do SQLAlchemy.
"""

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
SECRET_KEY = os.getenv("SECRET_KEY", os.getenv("SECURITY_KEY"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
