from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from model.schemas import LeadValidation
from model.Leads import LeadDB
from model.User import UserDB
from model.models import IdentityDB, UserLeadAssociation
from model.database import get_db
from routers.dependencies import (
    get_record,
)
import routers.dependencies

# from routers.dependencies import check_if_exists

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])

dependencies = routers.dependencies


@Cliente_routers.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/new_lead")
def new_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    # if dependencies.check_if_exists(db, LeadDB, "numero", data_lead):
    #     raise HTTPException(status_code=400, detail="O numero já está cadastrado.")
    # if dependencies.check_if_exists(db, IdentityDB, "numero", data_lead):
    #     raise HTTPException(
    #         status_code=400, detail="O numero já está cadastrado como usuario."
    #     )

    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User não encontrado.")
    new_lead = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero_lead,
        type="lead",
    )
    new_lead.users.append(existing_user)
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
def chat_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    # lead_is_exist_number => user_id passar a ser number id
    if not data_lead.numero_user:
        raise HTTPException(
            status_code=400, detail="É necessário informar o numero do usuario"
        )

    existing_lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)
    if not existing_lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado.")

    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)

    if not existing_user:
        raise HTTPException(status_code=404, detail="User não encontrado.")

    try:
        association = UserLeadAssociation(
            user_id=existing_user.id, lead_id=existing_lead.id
        )
        db.add(association)

        db.commit()
        return {
            "message": "Pareamento(s) criado(s) com sucesso",
            "lead_id": existing_lead.id,
            "usuarios_vinculados": existing_user.id,
        }
    except Exception as e:
        db.rollback()
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))
