from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from model.schemas import LeadValidation
from model.Leads import LeadDB
from model.User import UserDB
from model.models import IdentityDB, UserLeadAssociation
from model.database import get_db
from routers.dependencies import get_record, result_check, insert_db
import routers.dependencies

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])
dependencies = routers.dependencies


@Cliente_routers.get("/list-lead-in-user")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/new_lead")
def new_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):

    existing_lead = get_record(db, IdentityDB, {"numero": data_lead.numero_lead})
    result_check(existing_lead, "Numero ja cadastrado como user ou como lead.", 400)
    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    result_check(existing_user, "User não encontrado.", 404, False)

    new_lead = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero_lead,
        type="lead",
    )
    new_lead.users.append(existing_user)

    insert_db(db, new_lead, True)
    return {"message": "Novo Cliente criado com sucesso", "cliente_id": new_lead.id}


@Cliente_routers.post("/chat-lead")
def chat_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):

    result_check(
        data_lead.numero_user, "É necessário informar o numero de usuario.", 400, False
    )

    existing_lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)
    result_check(existing_lead, "Lead não encontrado.", 404, False)
    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    result_check(existing_user, "User não encontrado.", 404, False)

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
