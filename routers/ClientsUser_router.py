from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ClienteCreate
from ClientsUser import ClienteDB
from models import get_db

Cliente_routers = APIRouter(prefix="/clientes", tags=["clientes"])


@Cliente_routers.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    # Aqui sua lógica de consulta ao banco
    return {"mensagem": "Lista de clientes"}


@Cliente_routers.post("/add_cliente")
def add_cliente(data: ClienteCreate, db: Session = Depends(get_db)):
    # O SQLAlchemy, através do polimorfismo, insere na tabela 'usuarios' e 'clientes'
    # simultaneamente quando você cria o objeto com o tipo correto.
    novo_cliente = ClienteDB(
        name=data.name,
        numero=data.numero,
        admin_id=data.admin_id, # ID do admin que vem do n8n ou manual
        categoria=data.categoria,
        status=data.status,
        resumo_conversa=data.resumo_conversa,
        intencao=data.intencao,
        data_hora_servico=data.data_hora_servico,
        type="cliente" # Define a identidade polimórfica
    )

    try:
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return {"message": "Cliente criado com sucesso", "cliente_id": novo_cliente.id}
    except Exception as e:
        db.rollback()
        # Imprima o erro real para saber o que está acontecendo no banco
        print(f"ERRO DO SQLALCHEMY: {e}") 
        raise HTTPException(status_code=500, detail=str(e))