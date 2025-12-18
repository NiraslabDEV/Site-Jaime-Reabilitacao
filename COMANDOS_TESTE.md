# Comandos para Testar a API

## 1. Instalar dependências (se ainda não instalou)
```powershell
pip install -r requirements.txt
pip install 'pydantic[email]'
pip install requests
```

## 2. Iniciar o servidor

**Opção A - Terminal separado (recomendado):**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Opção B - Usando o script PowerShell:**
```powershell
.\start_and_test.ps1
```

## 3. Testar a API

**Com o script de teste:**
```powershell
python test_api.py
```

**Ou manualmente com curl/PowerShell:**

### Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
```

### Registrar usuário
```powershell
$body = @{
    email = "teste@example.com"
    password = "teste123456"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/auth/register" -Method POST -Body $body -ContentType "application/json"
```

### Login
```powershell
$body = @{
    email = "teste@example.com"
    password = "teste123456"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method POST -Body $body -ContentType "application/json"
$token = ($response.Content | ConvertFrom-Json).access_token
```

### Criar busca (substitua TOKEN pelo token recebido)
```powershell
$headers = @{
    Authorization = "Bearer TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    url = "https://fastapi.tiangolo.com"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/searches" -Method POST -Body $body -Headers $headers
```

### Listar buscas
```powershell
$headers = @{
    Authorization = "Bearer TOKEN"
}

Invoke-WebRequest -Uri "http://localhost:8000/searches" -Method GET -Headers $headers
```

## 4. Acessar documentação interativa

Abra no navegador:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

