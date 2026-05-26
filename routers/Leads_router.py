from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model.schemas import LeadsCreate
from model.Leads import LeadDB
from model.models import IdentityDB
from model.database import get_db
import dependencies

# from routers.dependencies import check_if_exists

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])


@Cliente_routers.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/new_lead")
def new_lead(data_lead: LeadsCreate, db: Session = Depends(get_db)):
    # TODO: Subistituir pela dependecia da função is_check esses metodos

    existing_lead_numero = (
        db.query(LeadDB).filter(LeadDB.numero == data_lead.numero).first()
    )
    if existing_lead_numero:
        raise HTTPException(status_code=400, detail="O numero já está cadastrado.")
    existing_numero = (
        db.query(IdentityDB).filter(IdentityDB.numero == data_lead.numero).first()
    )
    if existing_numero:
        raise HTTPException(
            status_code=400, detail="O numero já está cadastrado como usuario."
        )
    # criar o metodo de pode auterar o nivel de lead para user

    new_lead = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero,
        user_id=data_lead.user_id,  # ID do admin que vem do n8n ou manual
        categoria=data_lead.categoria,
        status=data_lead.status,
        resumo_conversa=data_lead.resumo_conversa,
        intencao=data_lead.intencao,
        data_hora_servico=data_lead.data_hora_servico,
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
