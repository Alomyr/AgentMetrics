from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# Importar depois de carregar as variáveis de ambiente (via config)
from model.database import engine, Base
from routers.Leads_router import Cliente_routers
from routers.User_router import user_routers
from routers.admin_router import admin_router
from model.models import Admin
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

# As variáveis vêm de config.py

app.include_router(Cliente_routers)
app.include_router(user_routers)
app.include_router(admin_router)


@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}
