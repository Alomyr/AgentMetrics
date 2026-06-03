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
- `requirements.txt` - dependências do projeto

## Endpoints principais

- `GET /` - verifica se a API está rodando
- `GET /leads/list-lead-in-user` - lista leads associados a usuários
- `POST /leads/chat-lead` - registra ou atualiza informações de lead e associação a usuário
- `POST /leads/aggregate-metricas` - agrega métricas de leads por usuário
- `GET /user/list-user` - lista usuários
- `POST /user/cadastro` - cadastra novo usuário
- `POST /user/validar-user` - valida credenciais de login
- `POST /user/nova-senha` - altera senha
- `POST /user/novo-email` - altera email
- `POST /user/novo-numero` - altera número
- `POST /user/novo-nome` - altera nome

> Observação: alguns endpoints ainda precisam de implementação completa e validações adicionais.

## Instalação

1. Clone o repositório

```bash
git clone https://github.com/Alomyr/AgentMetrics.git
cd AgentMetrics
```

2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

4. Configure seu banco de dados

A aplicação usa SQLAlchemy. Ajuste as variáveis de conexão em `model/database.py` conforme o banco que estiver usando.

## Execução

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Contribuição

Contribuições são bem-vindas. Abra issues ou pull requests para propor melhorias, correções ou novos recursos.

## Licença

Este projeto pode ser distribuído conforme a licença escolhida pelo mantenedor.
