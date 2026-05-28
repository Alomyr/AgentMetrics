from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from model.schemas import LeadsCreate, lead_is_exist_number
from model.Leads import LeadDB
from model.User import UserDB
from model.models import IdentityDB, UserLeadAssociation
from model.database import get_db
from routers.dependencies import check_if_exists, check_if_exists_login
import routers.dependencies

# from routers.dependencies import check_if_exists

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])

dependencies = routers.dependencies


@Cliente_routers.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/new_lead")
def new_lead(data_lead: LeadsCreate, db: Session = Depends(get_db)):
    if dependencies.check_if_exists(db, LeadDB, "numero", data_lead):
        raise HTTPException(status_code=400, detail="O numero já está cadastrado.")
    if dependencies.check_if_exists(db, IdentityDB, "numero", data_lead):
        raise HTTPException(
            status_code=400, detail="O numero já está cadastrado como usuario."
        )

    users = []
    if data_lead.user_ids:
        users = db.query(UserDB).filter(UserDB.id.in_(data_lead.user_ids)).all()
        if len(users) != len(data_lead.user_ids):
            raise HTTPException(
                status_code=404,
                detail="Um ou mais usuários associados ao lead não foram encontrados.",
            )

    new_lead = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero,
        users=users,
        type="lead",  # Define a identidade polimórfica
    )

    try:
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        return {"message": "Novo Cliente criado com sucesso", "cliente_id": new_lead.id}
    except Exception as e:
        db.rollback()
        # Imprima o erro real para saber o que está acontecendo no banco
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@Cliente_routers.post("/chat-lead")
def chat_lead(
    lead_is_exist_number: lead_is_exist_number, db: Session = Depends(get_db)
):

    if not lead_is_exist_number.user_ids:
        raise HTTPException(status_code=400, detail="É necessário informar user_ids.")

    existing_lead = check_if_exists_login(db, LeadDB, "numero", lead_is_exist_number)

    if not existing_lead.id:
        raise HTTPException(status_code=404, detail="Lead não encontrado.")

    users = db.query(UserDB).filter(UserDB.id.in_(lead_is_exist_number.user_ids)).all()
    
    if len(users) != len(lead_is_exist_number.user_ids):
        raise HTTPException(
            status_code=404, detail="Um ou mais usuários não foram encontrados."
        )

    try:
        for user in users:
            association = UserLeadAssociation(user_id=user.id, lead_id=existing_lead.id)
            db.add(association)

        db.commit()
        return {
            "message": "Pareamento(s) criado(s) com sucesso",
            "lead_id": existing_lead.id,
            "usuarios_vinculados": user.id,
        }
    except Exception as e:
        db.rollback()
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    else:
        return new_lead(lead_is_exist_number, db)
