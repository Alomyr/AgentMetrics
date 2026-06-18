from fastapi import FastAPI
from backend.src.core.database import engine, Base
from backend.src.leads.router import Cliente_routers
from backend.src.users.router import user_routers
from backend.src.admin.router import admin_router
from backend.src.admin.model import Admin

# Inicializa o Core da aplicação FastAPI
app = FastAPI(
    title="API de Gestão de Leads e Atendimentos",
    description="Sistema centralizado para controle de fluxos de chat, usuários e métricas operacionais.",
    version="1.0.0",
)

# Sincroniza e cria as tabelas do banco de dados relacional que ainda não existem
Base.metadata.create_all(bind=engine)

# Injeção e Registro de Rotas Globais
app.include_router(Cliente_routers)
app.include_router(user_routers)
app.include_router(admin_router)


@app.get("/", tags=["Health Check"])
def home():
    """
    Endpoint de Health Check (Verificação de Saúde do Sistema).

    Utilizado por ferramentas de monitoramento ou serviços de nuvem para
    confirmar se a instância do FastAPI está online e apta a receber tráfego.

    Returns:
        dict: Dicionário contendo o estado atual da API.
    """
    return {"status": "API rodando com sucesso"}
