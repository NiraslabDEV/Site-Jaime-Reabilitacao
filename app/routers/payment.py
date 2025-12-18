"""
Router para processamento de pagamentos M-Pesa
"""
from fastapi import APIRouter, HTTPException, status, Request
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/api/payment", tags=["payment"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
async def process_payment(payment_data: PaymentRequest):
    """
    Processa pagamento via M-Pesa.
    
    Este endpoint:
    1. Valida os dados do pagamento
    2. Inicia STK Push via API M-Pesa (mock ou real)
    3. Retorna transação pendente
    4. Aguarda callback de confirmação (processado em /callback)
    """
    try:
        return await PaymentService.process_payment(payment_data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao processar pagamento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar pagamento. Tente novamente mais tarde."
        )


@router.get("/status/{transaction_id}")
async def get_payment_status(transaction_id: str):
    """
    Consulta o status de um pagamento.
    
    Retorna o status atual da transação:
    - pending: Aguardando confirmação
    - success: Pagamento confirmado
    - failed: Pagamento falhou
    - expired: Tempo expirado
    """
    try:
        return await PaymentService.get_payment_status(transaction_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao consultar status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao consultar status do pagamento."
        )


@router.post("/callback")
async def mpesa_callback(request: Request):
    """
    Endpoint para receber callbacks da API M-Pesa.
    
    Este endpoint é chamado pela API M-Pesa quando:
    - O usuário confirma o pagamento
    - O pagamento expira
    - Ocorre um erro
    
    Em produção, deve validar a assinatura do callback.
    """
    try:
        callback_data = await request.json()
        
        # Processar callback
        success = await PaymentService.handle_mpesa_callback(callback_data)
        
        if success:
            return {
                "ResultCode": 0,
                "ResultDesc": "Callback processado com sucesso"
            }
        else:
            return {
                "ResultCode": 1,
                "ResultDesc": "Erro ao processar callback"
            }
            
    except Exception as e:
        print(f"Erro ao processar callback: {str(e)}")
        return {
            "ResultCode": 1,
            "ResultDesc": f"Erro: {str(e)}"
        }


# ============================================
# NOTAS PARA INTEGRAÇÃO REAL COM M-PESA
# ============================================
"""
Para integrar com M-Pesa real, você precisará:

1. Credenciais M-Pesa:
   - Consumer Key
   - Consumer Secret
   - Passkey
   - Business Short Code

2. Fluxo STK Push:
   a) Gerar access token (OAuth)
   b) Iniciar STK Push com:
      - Phone Number (formato: 258XXXXXXXX)
      - Amount
      - Account Reference
      - Transaction Description
   c) Receber callback de confirmação
   d) Validar e atualizar status

3. Bibliotecas úteis:
   - requests (para chamadas HTTP)
   - python-mpesa (biblioteca específica, se disponível)

4. Segurança:
   - Nunca exponha credenciais no frontend
   - Use variáveis de ambiente
   - Valide callbacks com assinatura
   - Implemente rate limiting
   - Use HTTPS sempre

5. Exemplo de estrutura de callback:
   {
       "Body": {
           "stkCallback": {
               "MerchantRequestID": "...",
               "CheckoutRequestID": "...",
               "ResultCode": 0,  # 0 = sucesso
               "ResultDesc": "The service request is processed successfully.",
               "CallbackMetadata": {
                   "Item": [
                       {"Name": "Amount", "Value": 450.00},
                       {"Name": "MpesaReceiptNumber", "Value": "..."},
                       {"Name": "PhoneNumber", "Value": 258841234567}
                   ]
               }
           }
       }
   }
"""

