from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from backend.src.leads.schemas import LeadValidation
from backend.src.leads.model import LeadDB
from backend.src.users.model import UserDB
from backend.src.leads.model import UserLeadAssociation
from backend.src.users.model import MetricasLeadInUser
from datetime import datetime
from backend.src.core.database import get_db
from backend.src.utils.validations import get_record, result_check, insert_db
import backend.src.utils.validations
from backend.src.leads.service import (
    modulo_lead,
    new_lead,
    validation_lead_user,
    lead_update,
    aggregate_metricas,
    edit_nome,
)

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])
dependencies = backend.src.utils.validations


@Cliente_routers.post("/chat-lead")
def chat_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    """
    Recebe os pacotes de conversão/interação vindos do webhook de chat.
    Decide se criará um novo lead, um novo pareamento ou se executará um update no histórico existente.
    """
    existing_lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)

    if not existing_lead:
        return "Lead não encontrado, adicionando ao sistema: ", new_lead(data_lead, db)

    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    result_check(existing_user, "User não encontrado.", 404, False)

    if existing_lead.name != data_lead.name:
        edit_nome(data_lead, db)

    association = validation_lead_user(existing_user, existing_lead, db, data_lead)

    if association:
        return (lead_update(data_lead, db, existing_user, existing_lead),)

    try:
        association_obj = modulo_lead(existing_user, existing_lead, data_lead)
        existing_lead.associations.append(association_obj)
        db.add(association_obj)
        db.commit()
        db.refresh(association_obj)

        return {
            "message": "Novo pareamento(s) criado(s) com sucesso",
            "lead_id": existing_lead.id,
            "usuarios_vinculados": existing_user.id,
            "Status": association_obj.status,
        }, aggregate_metricas(db)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
