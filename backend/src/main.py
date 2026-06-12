from fastapi import FastAPI
from backend.src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# Importar depois de carregar as variáveis de ambiente (via config)
from backend.src.core.database import engine, Base
from backend.src.leads.router import Cliente_routers
from backend.src.users.router import user_routers
from backend.src.admin.router import admin_router
from backend.src.admin.model import Admin
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
Base.metadata.create_all(bind=engine)

# As variáveis vêm de config.py

app.include_router(Cliente_routers)
app.include_router(user_routers)
app.include_router(admin_router)


@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}


# test
