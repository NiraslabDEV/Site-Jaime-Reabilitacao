# Script para iniciar o servidor e testar a API
Write-Host "Iniciando servidor FastAPI..." -ForegroundColor Green

# Iniciar servidor em background
$job = Start-Job -ScriptBlock {
    Set-Location 'c:\Users\Gabriel\Desktop\teste'
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Aguardar servidor iniciar
Write-Host "Aguardando servidor iniciar (5 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Executar testes
Write-Host "Executando testes..." -ForegroundColor Green
python test_api.py

# Parar o servidor
Write-Host "`nParando servidor..." -ForegroundColor Yellow
Stop-Job $job
Remove-Job $job

