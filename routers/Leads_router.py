from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model.schemas import LeadsCreate
from model.Leads import LeadDB
from model.models import get_db

Cliente_routers = APIRouter(prefix="/leads", tags=["Leads"])


@Cliente_routers.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/new_lead")
def new_lead(data: LeadsCreate, db: Session = Depends(get_db)):
    # O SQLAlchemy, através do polimorfismo, insere na tabela 'usuarios' e 'clientes'
    # simultaneamente quando você cria o objeto com o tipo correto.
    new_lead = LeadDB(
        name=data.name,
        numero=data.numero,
        user_id=data.user_id,  # ID do admin que vem do n8n ou manual
        categoria=data.categoria,
        status=data.status,
        resumo_conversa=data.resumo_conversa,
        intencao=data.intencao,
        data_hora_servico=data.data_hora_servico,
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
