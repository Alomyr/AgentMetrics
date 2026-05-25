from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from AdminUser import AdminDB
from schemas import AdminCreate

AdminUser_routers = APIRouter(prefix="/admin", tags=["admin"])


@AdminUser_routers.get("/")
def listar_admins(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de administradores"}


@AdminUser_routers.post("/add_admin")
def add_new_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    # 1. Crie o Admin
    novo_admin = AdminDB(
        name=admin_data.name,
        numero=admin_data.numero,
        email=admin_data.email,
        senha=admin_data.senha,
    )

    # Adicione ao banco
    db.add(novo_admin)

    # ADICIONE ESTA LINHA:
    # Isso força o SQLAlchemy a disparar o SQL agora e você verá o erro no terminal
    db.flush()

    db.commit()
    return {"message": "Sucesso"}
