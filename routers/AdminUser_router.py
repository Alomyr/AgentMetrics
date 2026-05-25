from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.models import get_db
from model.AdminUser import AdminDB
from model.schemas import AdminCreate

AdminUser_routers = APIRouter(prefix="/admin", tags=["admin"])


@AdminUser_routers.get("/")
def listar_admins(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de administradores"}


@AdminUser_routers.post("/add_admin")
def add_new_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    # Verifica se o email já existe antes de criar o admin
    existing_admin = db.query(AdminDB).filter(AdminDB.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="O email já está cadastrado.")

    novo_admin = AdminDB(
        name=admin_data.name,
        numero=admin_data.numero,
        email=admin_data.email,
        senha=admin_data.senha,
    )

    db.add(novo_admin)
    try:
        db.commit()
        db.refresh(novo_admin)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="O email já está cadastrado.")

    return {"message": "Sucesso", "admin_id": novo_admin.id}
