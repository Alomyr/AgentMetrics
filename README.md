# AgentMetrics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-blue?logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.3.0-purple?logo=vite)](https://vitejs.dev/)

> API de telemetria e gestão de leads desenvolvida para monitorar o consumo de recursos e metrificar o desempenho de agentes em tempo real.

## 📋 Visão Geral

**AgentMetrics** é uma aplicação fullstack (Python + React) que oferece um sistema centralizado para gerenciamento de usuários, leads e métricas operacionais. Construída com **FastAPI** (backend) e **React + Vite** (frontend), permite coletar, agregar e expor informações que ajudam a entender o comportamento e eficiência de agentes em um sistema de atendimento.

## ✨ Funcionalidades Principais

- ✅ **Gerenciamento de Usuários** - Cadastro, validação e autenticação JWT
- ✅ **Gestão de Leads** - Registro, associação a usuários e rastreamento
- ✅ **Painel Administrativo** - Controle centralizado de recursos
- ✅ **Autenticação Segura** - Tokens JWT com expiração configurável
- ✅ **API REST Completa** - Endpoints para consulta e atualização de dados
- ✅ **Persistência de Dados** - Banco de dados relacional via SQLAlchemy
- ✅ **Interface Web Responsiva** - Frontend moderno com React

## 🛠️ Stack Tecnológico

### Backend

- **Python 3.8+** - Linguagem base
- **FastAPI 0.136.1** - Framework web de alto desempenho
- **SQLAlchemy** - ORM para acesso a banco de dados
- **Pydantic** - Validação de dados
- **PyJWT & Passlib** - Autenticação e criptografia
- **Uvicorn** - Servidor ASGI
- **PostgreSQL/SQLite** - Banco de dados relacional

### Frontend

- **React 18.3.1** - Biblioteca UI
- **Vite 5.3.0** - Build tool e dev server
- **Axios** - Cliente HTTP
- **JavaScript/CSS3** - Estilos e interatividade

## 📁 Estrutura do Projeto

```
AgentMetrics/
├── backend/
│   ├── src/
│   │   ├── main.py                    # Inicialização da aplicação
│   │   ├── core/                      # Núcleo global da aplicação
│   │   │   ├── config.py              # Configurações e variáveis de ambiente
│   │   │   ├── database.py            # Conexão e setup do banco de dados
│   │   │   └── security.py            # Autenticação/Autorização JWT
│   │   ├── users/                     # Módulo de Usuários
│   │   │   ├── router.py              # Rotas de usuários
│   │   │   ├── model.py               # Modelo ORM User
│   │   │   └── schemas.py             # Schemas Pydantic para validação
│   │   ├── leads/                     # Módulo de Leads
│   │   │   ├── router.py              # Rotas de leads
│   │   │   ├── model.py               # Modelo ORM Lead
│   │   │   └── schemas.py             # Schemas Pydantic
│   │   ├── admin/                     # Módulo Administrativo
│   │   │   ├── router.py              # Rotas administrativas
│   │   │   ├── model.py               # Modelo ORM Admin
│   │   │   └── schemas.py             # Schemas administrativos
│   │   └── utils/                     # Utilitários globais
│   │       ├── enum.py                # Enumerações do projeto
│   │       ├── models.py              # Modelos compartilhados
│   │       ├── schemas.py             # Schemas comuns
│   │       └── validations.py         # Validações customizadas
│   ├── test/                          # Testes automatizados
│   │   ├── test_auth_flow.py          # Testes de autenticação
│   │   └── test.py                    # Testes gerais
│   ├── requirements.txt               # Dependências Python
│   ├── delet_test_sql.sql             # Script SQL para limpeza de testes
│   └── README.md                      # Documentação do backend
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx                   # Ponto de entrada React
│   │   ├── App.jsx                    # Componente raiz
│   │   ├── api.js                     # Cliente HTTP (Axios)
│   │   └── index.css                  # Estilos globais
│   ├── index.html                     # Template HTML
│   ├── package.json                   # Dependências Node.js
│   ├── vite.config.js                 # Configuração Vite
│   └── README.md                      # Documentação do frontend
│
├── doc/
│   ├── diagrama.drawio                # Diagramas da arquitetura
│   ├── env.txt                        # Template de variáveis de ambiente
│   └── NOTAS.md                       # Anotações e referências
│
├── LICENSE                            # Licença do projeto
└── README.md                          # Este arquivo
```

## 🚀 Quick Start

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 16+ e npm/yarn
- PostgreSQL 12+ (ou SQLite para desenvolvimento)
- Git

### Instalação do Backend

```bash
# Clonar repositório
git clone https://github.com/Alomyr/AgentMetrics.git
cd AgentMetrics/backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp ../doc/env.txt .env
# Editar .env com suas configurações
```

### Instalação do Frontend

```bash
cd ../frontend

# Instalar dependências
npm install
# ou
yarn install
```

### Rodar Aplicação Localmente

**Backend (Terminal 1):**

```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --port 8000
```

A API estará disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

**Frontend (Terminal 2):**

```bash
cd frontend
npm run dev
# ou
yarn dev
```

O frontend estará disponível em: `http://localhost:5173` (padrão Vite)

## 🔧 Configuração de Ambiente

Crie um arquivo `.env` na raiz do diretório `backend/` com as seguintes variáveis:

```env
# Segurança JWT
SECRET_KEY=sua_chave_secreta_muito_longa_aqui
SECURITY_KEY=sua_chave_de_seguranca
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Banco de Dados
SQLALCHEMY_DATABASE_URL=postgresql://usuario:senha@localhost:5432/agentmetrics
# Ou para SQLite (desenvolvimento):
# SQLALCHEMY_DATABASE_URL=sqlite:///./agentmetrics.db

# Aplicação
DEBUG=True
```

## 📚 Documentação da API

Uma vez que o backend está rodando, acesse:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

A documentação interativa gerada automaticamente pelo FastAPI permite testar todos os endpoints.

## 🧪 Testes

Executar testes automatizados:

```bash
cd backend

# Rodar todos os testes
pytest

# Rodar testes com cobertura
pytest --cov=src

# Rodar testes de fluxo de autenticação
pytest test/test_auth_flow.py -v
```

## 📦 Build para Produção

### Backend

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 src.main:app
```

### Frontend

```bash
cd frontend
npm run build
# Distribuir conteúdo de ./dist
```

## 🏗️ Arquitetura e Componentes

### Core Module (`src/core/`)

- **config.py** - Gerenciamento centralizado de configurações e variáveis de ambiente
- **database.py** - Inicialização do SQLAlchemy, session factory e declarative base
- **security.py** - Funções de hash de senha, validação e geração de tokens JWT

### Domain Modules (`src/users/`, `src/leads/`, `src/admin/`)

Cada módulo segue o padrão **MVC** com:

- **model.py** - Definição dos modelos SQLAlchemy (ORM)
- **schemas.py** - Schemas Pydantic para validação de entrada/saída
- **router.py** - Definição dos endpoints REST
- **service.py** (planejado) - Lógica de negócio isolada
- **dependencies.py** (planejado) - Injeção de dependências FastAPI

## 🔐 Autenticação e Autorização

O sistema utiliza **JWT (JSON Web Tokens)** para autenticação:

1. Usuário faz login e recebe um token
2. Token é enviado no header `Authorization: Bearer <token>` em requisições subsequentes
3. Backend valida o token e autoriza a requisição
4. Implementação em `src/core/security.py`

## 📊 Modelo de Dados

### User

```
- id: UUID (Primary Key)
- email: String (Unique)
- username: String (Unique)
- password_hash: String
- is_active: Boolean
- created_at: DateTime
```

### Lead

```
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- name: String
- email: String
- status: String (enum)
- created_at: DateTime
- updated_at: DateTime
```

### Admin

```
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- permissions: Array
- created_at: DateTime
```

## 🤝 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
2. Commit suas mudanças: `git commit -am 'Adiciona nova feature'`
3. Push para a branch: `git push origin feature/minha-feature`
4. Abra um Pull Request

## 📝 Próximas Melhorias

- [ ] Adicionar módulo `service.py` para cada domínio
- [ ] Implementar `dependencies.py` para injeção de dependências
- [ ] Adicionar logging global em `src/core/logging.py`
- [ ] Ampliar cobertura de testes
- [ ] Documentar fluxos de negócio no diagrama
- [ ] Implementar rate limiting
- [ ] Adicionar CI/CD com GitHub Actions
- [ ] Containerizar com Docker

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Alomyr**  
GitHub: [@Alomyr](https://github.com/Alomyr)

---

**Última atualização:** Junho 2026  
**Versão:** 1.0.0
                │   │   │── models.py
                │   │   │── schemas.py
                │   │   │── service.py
                │   │   │── dependencies.py
                │   │── admin/
                │   │   │── router.py
                │   │   │── models.py
                │   │   │── schemas.py
                │   │   │── service.py
                │   │── utils/
                │   │   │── enums.py
                │   │   │── helpers.py
                │── tests/
                │   │── users/
                │   │   │── test_users.py
                │   │── leads/
                │   │   │── test_leads.py
                │   │── admin/
                │   │   │── test_admin.py
                │── requirements.txt
                │── README.md

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

## Frontend React

O frontend está em `FrontEnd/` e usa React + Axios.

1. Vá para a pasta do frontend:

```bash
cd FrontEnd
```

1. Instale as dependências:

```bash
npm install
```

1. Inicie o frontend:

```bash
npm run dev
```

> O frontend já está configurado para proxy de `/api` para `http://127.0.0.1:8000`, então a FastAPI deve estar rodando em `http://127.0.0.1:8000`.

### Git e dependências

- Não commite `FrontEnd/node_modules/`.
- Commit apenas `FrontEnd/package.json`, `FrontEnd/package-lock.json`, `FrontEnd/src/`, `FrontEnd/vite.config.js` e `FrontEnd/index.html`.
- O `node_modules/` fica local; cada desenvolvedor instala com `npm install`.

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
