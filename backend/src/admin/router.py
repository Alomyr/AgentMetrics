# routers/admin_router.py
from fastapi import APIRouter, Depends, HTTPException
from requests import session
from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.admin.model import Admin
from backend.src.core.security import get_password_hash, verify_password
from backend.src.utils.validations import get_record, insert_db, result_check
from backend.src.admin.schemas import login_root

admin_router = APIRouter(prefix="/admin", tags=["Administração"])


@admin_router.post("/criar-root")
def criar_root(name: str, login: str, senha_plana: str, db: Session = Depends(get_db)):

    admin_login = get_record(db, Admin, {"login": login})
    result_check(admin_login, "Esse login ja existe", 400)
    senha_segura = get_password_hash(senha_plana)
    novo_admin = Admin(name=name, login=login, senha=senha_segura)
    insert_db(db, novo_admin, True)
    return {"message": "Admin criado com sucesso!", "login": login}


@admin_router.post("/validar-root")
def validar_root(login: login_root, db: Session = Depends(get_db)):

    admin = get_record(db, Admin, {"login": login.login}, True)
    result_check(admin, "Senha ou Login errados.", 400, False)

    if not verify_password(login.senha, admin.senha):
        raise HTTPException(status_code=400, detail="Senha ou Login errados")

    return {"message": "Autenticação bem-sucedida", "login": admin.login}
