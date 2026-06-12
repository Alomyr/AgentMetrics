from fastapi import FastAPI
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# Importar depois de carregar as variáveis de ambiente (via config)
from backend.model.database import engine, Base
from backend.routers.Leads_router import Cliente_routers
from backend.routers.User_router import user_routers
from backend.routers.admin_router import admin_router
from backend.model.models import Admin
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