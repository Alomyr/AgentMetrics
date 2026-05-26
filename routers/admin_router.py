# routers/admin_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model.database import get_db
from model.models import Admin
from model.security import get_password_hash

admin_router = APIRouter(prefix="/admin", tags=["Administração"])


@admin_router.post("/criar-root")
def criar_root(name: str, login: str, senha_plana: str, db: Session = Depends(get_db)):
    # 1. Verifica se já existe um admin com esse login
    if db.query(Admin).filter(Admin.login == login).first():
        raise HTTPException(status_code=400, detail="Este login já existe")

    # 2. Criptografa a senha antes de salvar
    senha_segura = get_password_hash(senha_plana)

    # 3. Salva no banco
    novo_admin = Admin(name=name, login=login, senha=senha_segura)
    db.add(novo_admin)
    db.commit()
    db.refresh(novo_admin)

    return {"message": "Admin criado com sucesso!", "login": login}
