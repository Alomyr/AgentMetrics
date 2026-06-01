from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from model.schemas import LeadValidation
from model.Leads import LeadDB
from model.User import UserDB
from model.models import IdentityDB, UserLeadAssociation, MetricasLeadInUser
from datetime import datetime
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
    return {
        "message": "Novo Cliente criado com sucesso",
        "cliente_id": new_lead.id,
    }, aggregate_metricas(
        db,
    )


def validation_lead_user(user, lead, db: Session):
    association = (
        db.query(UserLeadAssociation)
        .filter(
            UserLeadAssociation.lead_id == lead.id,
            UserLeadAssociation.user_id == user.id,
        )
        .first()
    )
    return association


def lead_update(data_lead, db: Session, user, lead):
    try:
        association = validation_lead_user(user, lead, db)

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
            }, aggregate_metricas(
                db,
            )

    except Exception as e:
        db.rollback()
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def aggregate_metrics_for_user(user: UserDB, db: Session):
    associations = (
        db.query(UserLeadAssociation)
        .filter(UserLeadAssociation.user_id == user.id)
        .all()
    )

    total_leads = len(associations)
    leads_abertos = sum(1 for a in associations if a.status == "ABERTO")
    leads_fechados = sum(1 for a in associations if a.status == "FECHADO")

    satisfacoes = [a.satisfacao for a in associations if a.satisfacao is not None]
    avg_satisfacao = float(sum(satisfacoes) / len(satisfacoes)) if satisfacoes else None

    # avg_response_time não está disponível nos dados atuais; guardar como None
    avg_response_time = None

    metric = (
        db.query(MetricasLeadInUser)
        .filter(MetricasLeadInUser.user_id == user.id)
        .first()
    )

    if metric:
        metric.total_leads = total_leads
        metric.leads_abertos = leads_abertos
        metric.leads_fechados = leads_fechados
        metric.avg_satisfacao = avg_satisfacao
        metric.avg_response_time = avg_response_time
        metric.last_aggregated = datetime.utcnow()
    else:
        metric = MetricasLeadInUser(
            user_id=user.id,
            total_leads=total_leads,
            leads_abertos=leads_abertos,
            leads_fechados=leads_fechados,
            avg_satisfacao=avg_satisfacao,
            avg_response_time=avg_response_time,
            last_aggregated=datetime.utcnow(),
        )
        db.add(metric)

    db.commit()
    db.refresh(metric)
    return metric


@Cliente_routers.post("/aggregate-metricas")
def aggregate_metricas(db: Session = Depends(get_db)):
    try:
        users = db.query(UserDB).all()
        results = []
        for u in users:
            m = aggregate_metrics_for_user(u, db)
            results.append(
                {
                    "user_id": u.id,
                    "total_leads": m.total_leads,
                    "leads_abertos": m.leads_abertos,
                    "leads_fechados": m.leads_fechados,
                    "avg_satisfacao": m.avg_satisfacao,
                    "last_aggregated": m.last_aggregated,
                }
            )

        return {"message": "Métricas agregadas com sucesso", "summary": results}
    except Exception as e:
        db.rollback()
        print(f"ERRO AO AGREGAR METRICAS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@Cliente_routers.post("/chat-lead")
def chat_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    existing_lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)

    if not existing_lead:
        return f"Lead não encontrado, adicionando o sistema: ", new_lead(data_lead, db)
    else:
        existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
        result_check(existing_user, "User não encontrado.", 404, False)

        association = validation_lead_user(existing_user, existing_lead, db)
        if association:
            return (lead_update(data_lead, db, existing_user, existing_lead),)

        try:
            association = modulo_lead(existing_user, existing_lead, data_lead)
            # anexar também à lista de associações do lead (mantém o estado ORM consistente)
            existing_lead.associations.append(association)
            db.add(association)
            db.commit()
            db.refresh(association)

            return {
                "message": "Novo pareamento(s) criado(s) com sucesso",
                "lead_id": existing_lead.id,
                "usuarios_vinculados": existing_user.id,
            }, aggregate_metricas(
                db,
            )

        except Exception as e:
            db.rollback()
            print(f"ERRO DO SQLALCHEMY: {e}")
            raise HTTPException(status_code=500, detail=str(e))
