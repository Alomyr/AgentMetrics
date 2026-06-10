# AgentMetrics

API de telemetria desenvolvida para monitorar o consumo de recursos e metrificar o desempenho de agentes em tempo real.

## Visão geral

`AgentMetrics` é uma API construída com FastAPI e SQLAlchemy para gerenciar dados de usuários, leads e métricas de desempenho de agentes. O projeto permite coletar, agregar e expor informações que ajudam a entender o comportamento e a eficiência de agentes em um sistema de atendimento.

## Funcionalidades principais

- Cadastro e validação de usuários
- Registro e associação de leads a usuários
- Agregação de métricas de desempenho por usuário
- Endpoints REST para consulta e atualização de dados
- Banco de dados relacional suportado via SQLAlchemy

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic
- PostgreSQL (`psycopg2-binary`) ou outro banco compatível com SQLAlchemy

## Estrutura básica

- `main.py` - inicialização da aplicação e registro de rotas
- `routers/` - rotas da API para `leads`, `user` e administração
- `model/` - definição do banco, modelos, esquemas, autenticação e validações
- `config.py` - define as variaveis de ambiente para a api
- `requirements.txt` - dependências do projeto
- `.env` - crie ou edite o arquinvo env configurando seu ambiente de criptografia e banco de dados, para caso de edição adicione um . antes do nome do arquivo env => .env

## Endpoints principais

- `GET /` - verifica se a API está rodando
- `GET /leads/list-lead-in-user` - lista leads associados a usuários
- `POST /leads/chat-lead` - registra ou atualiza informações de lead e associação a usuário
- `POST /leads/aggregate-metricas` - agrega métricas de leads por usuário
- `GET /user/list-user` - lista usuários
- `POST /user/cadastro` - cadastra novo usuário
- `POST /user/validar-user` - valida credenciais de login

> Observação: alguns endpoints ainda precisam de implementação completa e validações adicionais.

## Instalação

1. Clone o repositório

```bash
git clone https://github.com/Alomyr/AgentMetrics.git
cd AgentMetrics
```

1. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Instale as dependências

```bash
pip install -r requirements.txt
```

1. Configure seu banco de dados

A aplicação usa SQLAlchemy. Ajuste as variáveis de conexão em `model/database.py` conforme o banco que estiver usando.

## Execução

```bash
uvicorn main:app --reload
```

#### nomes paddrao de variaveis de ambiente

```
SQLALCHEMY_DATABASE_URL="seu link com seu banco de dados deve vim aqui"
SECRET_KEY=SUA CHAVE SECRETA
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Contribuição

Contribuições são bem-vindas. Abra issues ou pull requests para propor melhorias, correções ou novos recursos.

## Licença

Este projeto pode ser distribuído conforme a licença escolhida pelo mantenedor.
