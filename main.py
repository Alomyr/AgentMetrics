from fastapi import FastAPI
from model.models import engine, Base
from routers.Leads_router import Cliente_routers
from routers.User_router import user_routers

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(Cliente_routers)
app.include_router(user_routers)


@app.get("/")
def home():
    return {"status": "API rodando com sucesso"}
