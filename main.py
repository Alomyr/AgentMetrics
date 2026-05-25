from fastapi import FastAPI
from models import engine, Base
from routers.ClientsUser_router import Cliente_routers
from routers.AdminUser_router import AdminUser_routers

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(Cliente_routers)
app.include_router(AdminUser_routers)


@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}
