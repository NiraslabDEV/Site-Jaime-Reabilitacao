# Script PowerShell para testar a integração completa
# Execute: .\testar_integracao.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "TESTE DE INTEGRAÇÃO - LOJA VIRTUAL M-PESA" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar se Python está instalado
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python não encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python 3.12 ou superior" -ForegroundColor Red
    exit 1
}

# Verificar se o servidor está rodando
Write-Host "`n2. Verificando servidor..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 3 -ErrorAction Stop
    Write-Host "   ✓ Servidor está rodando na porta 8000" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Servidor não está rodando!" -ForegroundColor Red
    Write-Host "`n   Iniciando servidor..." -ForegroundColor Yellow
    
    # Tentar iniciar o servidor em background
    $env:PYTHONUNBUFFERED = "1"
    Start-Process python -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" -WindowStyle Hidden
    
    Write-Host "   Aguardando servidor iniciar..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Verificar novamente
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 3 -ErrorAction Stop
        Write-Host "   ✓ Servidor iniciado com sucesso!" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ Não foi possível iniciar o servidor automaticamente" -ForegroundColor Red
        Write-Host "`n   Execute manualmente:" -ForegroundColor Yellow
        Write-Host "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
        exit 1
    }
}

# Executar testes automatizados
Write-Host "`n3. Executando testes automatizados..." -ForegroundColor Yellow
Write-Host "   (Isso pode levar alguns segundos)`n" -ForegroundColor Gray

try {
    python test_payment_api.py
    $testExitCode = $LASTEXITCODE
    
    if ($testExitCode -eq 0) {
        Write-Host "`n✓ Todos os testes passaram!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Alguns testes falharam" -ForegroundColor Red
    }
} catch {
    Write-Host "`n✗ Erro ao executar testes: $_" -ForegroundColor Red
}

# Abrir página de teste frontend
Write-Host "`n4. Abrindo página de teste frontend..." -ForegroundColor Yellow
$testFrontendPath = Join-Path $PSScriptRoot "test_frontend.html"

if (Test-Path $testFrontendPath) {
    Start-Process $testFrontendPath
    Write-Host "   ✓ Página de teste aberta no navegador" -ForegroundColor Green
} else {
    Write-Host "   ✗ Arquivo test_frontend.html não encontrado" -ForegroundColor Red
}

# Abrir landing page principal
Write-Host "`n5. Abrindo landing page principal..." -ForegroundColor Yellow
$indexPath = Join-Path $PSScriptRoot "index.html"

if (Test-Path $indexPath) {
    Start-Process $indexPath
    Write-Host "   ✓ Landing page aberta no navegador" -ForegroundColor Green
} else {
    Write-Host "   ✗ Arquivo index.html não encontrado" -ForegroundColor Red
}

# Resumo
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "RESUMO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nServidor: http://localhost:8000" -ForegroundColor White
Write-Host "Documentação API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Teste Frontend: test_frontend.html" -ForegroundColor White
Write-Host "Landing Page: index.html" -ForegroundColor White
Write-Host "`nPara parar o servidor, pressione Ctrl+C no terminal onde ele está rodando" -ForegroundColor Yellow
Write-Host "`n"





