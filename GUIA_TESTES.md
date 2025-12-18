# 🧪 Guia de Testes - Integração M-Pesa

Guia completo para testar a integração de pagamento M-Pesa.

## 📋 Pré-requisitos

1. Python 3.12+ instalado
2. Dependências instaladas: `pip install -r requirements.txt`
3. Servidor FastAPI rodando (ou use o script de teste)

## 🚀 Formas de Testar

### Opção 1: Script Automatizado (Recomendado)

Execute o script PowerShell que faz tudo automaticamente:

```powershell
.\testar_integracao.ps1
```

Este script:
- ✅ Verifica se o servidor está rodando
- ✅ Inicia o servidor se necessário
- ✅ Executa testes automatizados
- ✅ Abre páginas de teste no navegador

### Opção 2: Teste Python Automatizado

Execute os testes automatizados:

```bash
python test_payment_api.py
```

**O que é testado:**
1. Conectividade do servidor
2. Pagamento bem-sucedido
3. Validações (valor, telefone, etc.)
4. Múltiplos pagamentos simultâneos

### Opção 3: Página de Teste Frontend

Abra `test_frontend.html` no navegador para testar via interface:

- Teste de conectividade
- Processar pagamento
- Consultar status

### Opção 4: Teste Manual via cURL

#### 1. Verificar saúde do servidor:
```bash
curl http://localhost:8000/health
```

#### 2. Processar pagamento:
```bash
curl -X POST "http://localhost:8000/api/payment" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 450.00,
    "phone_number": "841234567",
    "order_reference": "TEST-001"
  }'
```

#### 3. Consultar status:
```bash
curl "http://localhost:8000/api/payment/status/TXN-XXXXXXXX"
```

### Opção 5: Teste via Interface da Loja

1. Abra `index.html` no navegador
2. Adicione produtos ao carrinho
3. Clique em "Pagar com M-Pesa"
4. Preencha o número de telefone
5. Confirme o pagamento

## 📊 Resultados Esperados

### Teste de Pagamento Bem-Sucedido

**Request:**
```json
{
  "amount": 450.00,
  "phone_number": "841234567",
  "order_reference": "ORD-123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Pagamento iniciado. Confirme no seu telefone.",
  "transaction_id": "TXN-XXXXXXXX",
  "order_reference": "ORD-123",
  "amount": 450.00,
  "phone_number": "841234567",
  "status": "pending",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Teste de Validação (Valor Inválido)

**Request:**
```json
{
  "amount": 0.5,
  "phone_number": "841234567",
  "order_reference": "ORD-123"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Valor mínimo de pagamento é 1 MTZ"
}
```

### Teste de Validação (Telefone Inválido)

**Request:**
```json
{
  "amount": 450.00,
  "phone_number": "123456789",
  "order_reference": "ORD-123"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Número de telefone inválido. Use um número M-Pesa válido..."
}
```

## 🔍 Verificações

### ✅ Checklist de Testes

- [ ] Servidor responde em `/health`
- [ ] Pagamento com dados válidos retorna sucesso
- [ ] Validação de valor mínimo funciona
- [ ] Validação de telefone funciona
- [ ] Consulta de status funciona
- [ ] Múltiplos pagamentos simultâneos funcionam
- [ ] Frontend consegue se comunicar com API
- [ ] Carrinho persiste no localStorage
- [ ] Notificações aparecem corretamente

## 🐛 Troubleshooting

### Erro: "Connection refused"

**Problema:** Servidor não está rodando

**Solução:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Erro: "Module not found"

**Problema:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "CORS error" no frontend

**Problema:** CORS não configurado

**Solução:** O backend já está configurado com CORS. Verifique se está usando `http://localhost:8000`

### Erro: "UnicodeEncodeError" no Windows

**Problema:** Encoding do terminal Windows

**Solução:** Execute com:
```bash
chcp 65001
python test_payment_api.py
```

## 📝 Notas

- Os pagamentos são **simulados** (mock)
- Taxa de sucesso: ~85% (configurável)
- Transações são armazenadas em memória (não persistem após reiniciar)
- Para produção, substitua o mock pela API real M-Pesa

## 🎯 Próximos Passos

Após validar os testes:

1. ✅ Integração funcionando
2. 🔄 Substituir mock por API real M-Pesa
3. 🔄 Adicionar banco de dados para persistência
4. 🔄 Implementar callbacks reais
5. 🔄 Adicionar autenticação
6. 🔄 Configurar webhooks

---

**Boa sorte com os testes!** 🚀





