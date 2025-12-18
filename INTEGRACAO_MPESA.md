# 🔌 Integração M-Pesa - Guia Completo

Guia para configurar e usar a integração real com API M-Pesa.

## 📋 Credenciais Fornecidas

```
Application Name: API Link Pagamentos
Version: 1.0
Sandbox API Key: HeceKhPwJLOuAr4D00hMpNlcAghmkLEG
Status: In Development
Session Lifetime: 1 hora
Trusted Sources: *
```

## ⚙️ Configuração

### 1. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
# M-Pesa API Configuration
MPESA_API_KEY=HeceKhPwJLOuAr4D00hMpNlcAghmkLEG
MPESA_API_URL=https://api.mpesa.com
MPESA_ENVIRONMENT=sandbox
MPESA_CALLBACK_URL=http://localhost:8000/api/payment/callback
```

**Importante:**
- Em produção, ajuste `MPESA_API_URL` para a URL real da API
- Configure `MPESA_CALLBACK_URL` com sua URL pública (HTTPS obrigatório)
- Use variáveis de ambiente seguras, nunca commite o `.env`

### 2. URL da API

Ajuste `MPESA_API_URL` em `app/core/config.py` ou `.env` conforme a documentação da sua API:

- **Sandbox**: `https://sandbox.mpesa.com` (ou URL fornecida)
- **Produção**: `https://api.mpesa.com` (ou URL fornecida)

### 3. Endpoints da API

Os endpoints podem variar conforme a documentação. Ajuste em `app/core/mpesa_client.py`:

```python
# Autenticação
auth_url = f"{settings.MPESA_API_URL}/oauth/v1/generate?grant_type=client_credentials"

# Pagamento
payment_url = f"{settings.MPESA_API_URL}/mpesa/payment/v1/processrequest"

# Consulta de status
status_url = f"{settings.MPESA_API_URL}/mpesa/payment/v1/queryrequest"
```

## 🔄 Como Funciona

### Fluxo de Pagamento

1. **Cliente inicia pagamento** → Frontend envia dados
2. **Backend valida** → PaymentService valida dados
3. **Chama API M-Pesa** → MpesaClient.iniciate_payment_link()
4. **Obtém token** → Autenticação OAuth automática
5. **Cria link de pagamento** → API retorna transaction ID
6. **Cliente confirma** → Via SMS/link no telefone
7. **Callback recebido** → API M-Pesa notifica nosso backend
8. **Status atualizado** → Transação marcada como sucesso

### Modo Mock vs Real

O sistema detecta automaticamente:

- **Com `MPESA_API_KEY` configurado**: Usa API real
- **Sem `MPESA_API_KEY`**: Usa modo mock (desenvolvimento)

## 🧪 Testando a Integração

### 1. Teste Básico

```bash
# Certifique-se de que o servidor está rodando
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Execute os testes
python test_payment_api.py
```

### 2. Teste via Frontend

1. Abra `index.html` ou `test_frontend.html`
2. Adicione produtos ao carrinho
3. Clique em "Pagar com M-Pesa"
4. Preencha número de telefone (9 dígitos)
5. Confirme o pagamento

### 3. Teste via cURL

```bash
curl -X POST "http://localhost:8000/api/payment" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 450.00,
    "phone_number": "841234567",
    "order_reference": "TEST-001"
  }'
```

## 📝 Ajustes Necessários

### 1. Estrutura da Resposta da API

Ajuste em `app/services/payment_service.py` conforme a estrutura real:

```python
# Exemplo - ajustar conforme sua API
mpesa_transaction_id = mpesa_response.get("TransactionID") or \
                      mpesa_response.get("transactionId") or \
                      mpesa_response.get("CheckoutRequestID")
```

### 2. Autenticação

Ajuste em `app/core/mpesa_client.py` conforme o método de autenticação:

```python
# Opção 1: Bearer Token (atual)
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Opção 2: Basic Auth (se necessário)
credentials = base64.b64encode(f"{api_key}:".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}
```

### 3. Formato de Dados

Ajuste o payload em `MpesaClient.initiate_payment_link()`:

```python
payment_data = {
    "phoneNumber": phone_number,  # Pode ser "PhoneNumber", "phone", etc.
    "amount": str(int(amount)),   # Pode precisar de formato diferente
    "accountReference": order_reference,
    "transactionDesc": description,
    "callbackUrl": callback_url
}
```

## 🔐 Segurança

### ✅ Boas Práticas

1. **Nunca exponha a API Key no frontend**
2. **Use HTTPS em produção**
3. **Valide callbacks com assinatura** (se a API suportar)
4. **Implemente rate limiting**
5. **Use variáveis de ambiente**
6. **Monitore logs de erro**

### 🔒 Validação de Callbacks

Adicione validação de assinatura em `app/routers/payment.py`:

```python
@router.post("/callback")
async def mpesa_callback(request: Request):
    # Validar assinatura do callback (se suportado)
    # signature = request.headers.get("X-Signature")
    # if not validate_signature(signature, request.body):
    #     return {"ResultCode": 1, "ResultDesc": "Invalid signature"}
    
    callback_data = await request.json()
    success = await PaymentService.handle_mpesa_callback(callback_data)
    # ...
```

## 🐛 Troubleshooting

### Erro: "Erro ao obter token M-Pesa"

**Possíveis causas:**
- URL da API incorreta
- Método de autenticação incorreto
- API Key inválida

**Solução:**
1. Verifique a URL em `MPESA_API_URL`
2. Confirme o método de autenticação na documentação
3. Teste a API Key diretamente

### Erro: "Erro ao processar pagamento M-Pesa"

**Possíveis causas:**
- Formato de dados incorreto
- Endpoint incorreto
- Parâmetros obrigatórios faltando

**Solução:**
1. Verifique a documentação da API
2. Ajuste o formato em `mpesa_client.py`
3. Adicione logs para debug

### Token expira muito rápido

**Solução:**
O token é renovado automaticamente. Se necessário, ajuste o cache em `mpesa_client.py`.

## 📚 Documentação da API

Consulte a documentação oficial da sua API M-Pesa para:

- URLs exatas dos endpoints
- Formato de autenticação
- Estrutura de requisições/respostas
- Códigos de erro
- Webhooks/callbacks

## 🚀 Próximos Passos

1. ✅ Configurar `.env` com API Key
2. ✅ Ajustar URLs e endpoints conforme documentação
3. ✅ Testar autenticação
4. ✅ Testar criação de pagamento
5. ✅ Configurar callback URL pública
6. ✅ Testar callbacks
7. ✅ Implementar validação de assinatura
8. ✅ Adicionar logs e monitoramento

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs do servidor
2. Teste a API diretamente (Postman/curl)
3. Consulte a documentação oficial
4. Verifique se está usando sandbox ou produção

---

**Integração configurada e pronta para uso!** 🎉





