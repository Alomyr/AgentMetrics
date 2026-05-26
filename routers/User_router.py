from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.models import get_db
from model.User import UserDB
from model.schemas import Creat_new_user

user_routers = APIRouter(prefix="/user", tags=["User"])


@user_routers.get("/")
def listar_admins(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de administradores"}


@user_routers.post("/cadastro")
def add_new_user(user_data: Creat_new_user, db: Session = Depends(get_db)):
    # Verifica se o email já existe antes de criar o admin
    existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="O email já está cadastrado.")

    novo_user = UserDB(
        name=user_data.name,
        numero=user_data.numero,
        email=user_data.email,
        senha=user_data.senha,
    )

    db.add(novo_user)
    try:
        db.commit()
        db.refresh(novo_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="O email já está cadastrado.")

    return {"message": "Sucesso", "user_id": novo_user.id}
