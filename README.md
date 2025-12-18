# Technical Documentation Analyzer - Backend API

Backend API desenvolvido em Python com FastAPI, Supabase e JWT para autenticação.

## 📋 Requisitos

- Python 3.12 ou superior
- Conta no Supabase (https://supabase.com)
- Docker (opcional, para execução via container)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd teste
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
JWT_SECRET=your_jwt_secret_key_here_minimum_32_characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Onde obter as credenciais do Supabase:**
1. Acesse https://supabase.com
2. Crie um novo projeto ou use um existente
3. Vá em Settings > API
4. Copie a `URL` e a `anon key` (ou `service_role key`)

**JWT_SECRET:**
- Use uma string aleatória segura com pelo menos 32 caracteres
- Você pode gerar uma usando: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

## 🗄️ Configuração do Supabase

### Criar as tabelas

Execute os seguintes comandos SQL no SQL Editor do Supabase:

#### Tabela `users`:

```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índice para busca rápida por email
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

#### Tabela `searches`:

```sql
CREATE TABLE IF NOT EXISTS searches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índice para busca rápida por user_id
CREATE INDEX IF NOT EXISTS idx_searches_user_id ON searches(user_id);

-- Criar índice para ordenação por created_at
CREATE INDEX IF NOT EXISTS idx_searches_created_at ON searches(created_at DESC);
```

## ▶️ Executando a aplicação

### Modo de desenvolvimento

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

### Documentação interativa

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐳 Executando com Docker

### 1. Construir a imagem

```bash
docker build -t docs-analyzer-api .
```

### 2. Executar o container

```bash
docker run -p 8000:8000 --env-file .env docs-analyzer-api
```

## 📡 Endpoints da API

### Autenticação

#### POST `/auth/register`
Registra um novo usuário.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

#### POST `/auth/login`
Faz login e recebe um token JWT.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Buscas (Autenticado)

#### GET `/searches`
Retorna as últimas 20 buscas do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
    {
        "id": "uuid",
        "user_id": "uuid",
        "url": "https://example.com/docs",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

#### POST `/searches`
Salva uma nova URL de documentação.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
    "url": "https://example.com/docs"
}
```

**Response:**
```json
{
    "id": "uuid",
    "user_id": "uuid",
    "url": "https://example.com/docs",
    "created_at": "2024-01-01T00:00:00Z"
}
```

#### DELETE `/searches/{search_id}`
Deleta uma busca específica.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** 204 No Content

## 🔒 Autenticação

Todos os endpoints de `/searches` requerem autenticação via JWT.

Para usar os endpoints protegidos, inclua o header:
```
Authorization: Bearer <seu_token_jwt>
```

O token expira após 24 horas (configurável via `JWT_EXPIRATION_HOURS`).

## 🏗️ Estrutura do Projeto

```
app/
├── core/           # Configurações e utilitários centrais
│   ├── config.py      # Configurações da aplicação
│   ├── security.py    # Funções de segurança (JWT, bcrypt)
│   └── database.py    # Cliente Supabase
├── models/         # Modelos de dados
│   ├── user.py
│   └── search.py
├── schemas/        # Schemas Pydantic para validação
│   ├── auth.py
│   ├── user.py
│   └── search.py
├── services/       # Lógica de negócio
│   ├── auth_service.py
│   └── search_service.py
├── routers/        # Endpoints da API
│   ├── auth.py
│   ├── searches.py
│   └── dependencies.py
└── main.py         # Aplicação FastAPI principal
```

## 🧪 Testando a API

### Exemplo com curl

**Registrar usuário:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

**Criar busca (substitua TOKEN pelo token recebido):**
```bash
curl -X POST "http://localhost:8000/searches" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com"}'
```

**Listar buscas:**
```bash
curl -X GET "http://localhost:8000/searches" \
  -H "Authorization: Bearer TOKEN"
```

## 📝 Notas

- As senhas são hasheadas com bcrypt antes de serem armazenadas
- Os tokens JWT usam o algoritmo HS256
- A API está preparada para receber módulos de scraping e AI no futuro
- A estrutura segue princípios de arquitetura limpa

## 🐛 Troubleshooting

### Erro: "SUPABASE_URL not found"
- Verifique se o arquivo `.env` existe e contém todas as variáveis necessárias

### Erro: "Invalid authentication credentials"
- Verifique se o token JWT não expirou
- Certifique-se de incluir o header `Authorization: Bearer <token>`

### Erro ao conectar ao Supabase
- Verifique se as credenciais estão corretas
- Certifique-se de que as tabelas foram criadas no Supabase

## 📄 Licença

Este projeto é privado e proprietário.
