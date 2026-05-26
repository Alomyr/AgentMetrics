from fastapi import FastAPI
from model.database import engine, Base
from routers.Leads_router import Cliente_routers
from routers.User_router import user_routers
from routers.admin_router import admin_router
from model.models import Admin

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(Cliente_routers)
app.include_router(user_routers)
app.include_router(admin_router)


@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}
