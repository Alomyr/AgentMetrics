from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()


@app.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui você usaria o db para fazer consultas
    return {"mensagem": "Conexão com banco estabelecida!"}
