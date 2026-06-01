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


def modulo_lead(existing_user, existing_lead, data_lead):
    association = UserLeadAssociation(
        user_id=existing_user.id,
        lead_id=existing_lead.id,
        categoria=data_lead.categoria,
        status=(data_lead.status.value if data_lead.status else None),
        resumo_conversa=data_lead.resumo_conversa,
        intencao=data_lead.intencao,
        data_hora_servico=data_lead.data_hora_servico,
        satisfacao=data_lead.satisfacao,
    )
    return association


def new_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):

    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    result_check(existing_user, "User não encontrado.", 404, False)

    new_lead = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero_lead,
        type="lead",
    )
    association = modulo_lead(existing_user, new_lead, data_lead)
    new_lead.associations.append(association)

    insert_db(db, new_lead, True)
    return {"message": "Novo Cliente criado com sucesso", "cliente_id": new_lead.id}


def lead_update(data_lead, db: Session, user, lead):
    try:
        association = (
            db.query(UserLeadAssociation)
            .filter(
                UserLeadAssociation.lead_id == lead.id,
                UserLeadAssociation.user_id == user.id,
            )
            .first()
        )
        if association:
            association.categoria = data_lead.categoria
            association.status = data_lead.status.value if data_lead.status else None
            association.resumo_conversa = data_lead.resumo_conversa
            association.intencao = data_lead.intencao
            association.data_hora_servico = data_lead.data_hora_servico
            association.satisfacao = data_lead.satisfacao

            db.commit()
            db.refresh(association)

            return {
                "message": "Pareamento atualizado com sucesso",
                "lead_id": lead.id,
                "usuario_vinculado": user.id,
            }
    except Exception as e:
        db.rollback()
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@Cliente_routers.post("/chat-lead")
def chat_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    existing_lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)

    if not existing_lead:
        return f"Lead não encontrado, adicionando o sistema: ", new_lead(data_lead, db)
    else:
        existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
        result_check(existing_user, "User não encontrado.", 404, False)

        if existing_lead.id and existing_user.id:
            return lead_update(data_lead, db, existing_user, existing_lead)
        else:
            try:
                association = modulo_lead(existing_user, existing_lead, data_lead)
                db.add(association)
                db.commit()
                return {
                    "message": "Novo pareamento(s) criado(s) com sucesso",
                    "lead_id": existing_lead.id,
                    "usuarios_vinculados": existing_user.id,
                }

            except Exception as e:
                db.rollback()
                print(f"ERRO DO SQLALCHEMY: {e}")
                raise HTTPException(status_code=500, detail=str(e))
