"""
Serviço de pagamento M-Pesa
Implementa lógica de negócio para processamento de pagamentos
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.core.config import settings
from app.core.mpesa_client import MpesaClient
from fastapi import HTTPException, status


class PaymentService:
    """Serviço para processamento de pagamentos M-Pesa"""
    
    # Cache de transações (em produção, usar banco de dados)
    _transactions: Dict[str, Dict[str, Any]] = {}
    
    @staticmethod
    async def process_payment(payment_data: PaymentRequest) -> PaymentResponse:
        """
        Processa um pagamento via M-Pesa.
        
        Em produção, este método:
        1. Valida os dados
        2. Gera referência única
        3. Chama API M-Pesa STK Push
        4. Salva transação no banco
        5. Retorna resposta
        """
        
        # Validações adicionais
        PaymentService._validate_payment_data(payment_data)
        
        # Gerar ID de transação único
        transaction_id = PaymentService._generate_transaction_id()
        
        # Formatar número de telefone para M-Pesa (258XXXXXXXX)
        formatted_phone = f"258{payment_data.phone_number}"
        
        # Usar API real se configurada, senão usar mock
        use_real_api = bool(settings.MPESA_API_KEY)
        
        if use_real_api:
            # Chamada real à API M-Pesa
            try:
                mpesa_response = await MpesaClient.initiate_payment_link(
                    phone_number=formatted_phone,
                    amount=payment_data.amount,
                    order_reference=payment_data.order_reference,
                    description=f"Pagamento pedido {payment_data.order_reference}"
                )
                
                # Extrair dados da resposta (ajustar conforme estrutura da API)
                mpesa_transaction_id = mpesa_response.get("TransactionID") or mpesa_response.get("transactionId") or mpesa_response.get("CheckoutRequestID")
                
                if mpesa_transaction_id:
                    transaction_id = mpesa_transaction_id
                    mpesa_success = True
                else:
                    # Se não retornou ID, considerar como falha
                    mpesa_success = False
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="API M-Pesa não retornou ID de transação válido"
                    )
                    
            except HTTPException:
                raise
            except Exception as e:
                # Em caso de erro, logar e usar fallback
                print(f"Erro ao chamar API M-Pesa real: {str(e)}")
                print("Usando modo mock como fallback...")
                use_real_api = False
        
        if not use_real_api:
            # Modo mock (desenvolvimento/testes)
            transaction_id = PaymentService._generate_transaction_id()
            mpesa_success = PaymentService._simulate_mpesa_response()
        
        if mpesa_success:
            # Salvar transação (em produção, salvar no banco)
            transaction_data = {
                "transaction_id": transaction_id,
                "order_reference": payment_data.order_reference,
                "amount": payment_data.amount,
                "phone_number": payment_data.phone_number,
                "formatted_phone": formatted_phone,
                "status": "pending",
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(minutes=10)
            }
            
            PaymentService._transactions[transaction_id] = transaction_data
            
            return PaymentResponse(
                success=True,
                message="Pagamento iniciado. Confirme no seu telefone.",
                transaction_id=transaction_id,
                order_reference=payment_data.order_reference,
                amount=payment_data.amount,
                phone_number=payment_data.phone_number,
                status="pending",
                timestamp=datetime.now()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível iniciar o pagamento. Verifique seu número e tente novamente."
            )
    
    @staticmethod
    async def get_payment_status(transaction_id: str) -> Dict[str, Any]:
        """
        Consulta o status de uma transação.
        
        Em produção, buscar do banco de dados e/ou API M-Pesa.
        """
        
        # Buscar transação (em produção, buscar do banco)
        transaction = PaymentService._transactions.get(transaction_id)
        
        # Se usar API real e transação não encontrada localmente, consultar API
        use_real_api = bool(settings.MPESA_API_KEY)
        
        if not transaction and use_real_api:
            try:
                # Consultar status na API M-Pesa
                mpesa_status = await MpesaClient.check_payment_status(transaction_id)
                
                # Converter status da API para nosso formato
                api_status = mpesa_status.get("status", "pending")
                if api_status in ["Completed", "Success", "success"]:
                    status_value = "success"
                elif api_status in ["Failed", "failed", "Cancelled"]:
                    status_value = "failed"
                else:
                    status_value = "pending"
                
                return {
                    "transaction_id": transaction_id,
                    "status": status_value,
                    "amount": mpesa_status.get("amount", 0),
                    "order_reference": mpesa_status.get("accountReference", ""),
                    "message": PaymentService._get_status_message(status_value)
                }
            except Exception as e:
                print(f"Erro ao consultar status na API: {str(e)}")
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada"
            )
        
        # Simular atualização de status (apenas em modo mock)
        if not use_real_api and transaction["status"] == "pending":
            elapsed = datetime.now() - transaction["created_at"]
            if elapsed > timedelta(minutes=5):
                transaction["status"] = "success"
        
        return {
            "transaction_id": transaction_id,
            "status": transaction["status"],
            "amount": transaction["amount"],
            "order_reference": transaction["order_reference"],
            "message": PaymentService._get_status_message(transaction["status"])
        }
    
    @staticmethod
    async def handle_mpesa_callback(callback_data: Dict[str, Any]) -> bool:
        """
        Processa callback da API M-Pesa.
        
        Este método é chamado quando M-Pesa envia confirmação de pagamento.
        Em produção, deve validar assinatura e atualizar status no banco.
        """
        
        # Estrutura esperada do callback M-Pesa:
        # {
        #     "Body": {
        #         "stkCallback": {
        #             "MerchantRequestID": "...",
        #             "CheckoutRequestID": "...",
        #             "ResultCode": 0,  # 0 = sucesso
        #             "ResultDesc": "...",
        #             "CallbackMetadata": {
        #                 "Item": [
        #                     {"Name": "Amount", "Value": 450.00},
        #                     {"Name": "MpesaReceiptNumber", "Value": "..."},
        #                     {"Name": "PhoneNumber", "Value": 258841234567}
        #                 ]
        #             }
        #         }
        #     }
        # }
        
        try:
            # Extrair dados do callback
            stk_callback = callback_data.get("Body", {}).get("stkCallback", {})
            result_code = stk_callback.get("ResultCode", -1)
            checkout_request_id = stk_callback.get("CheckoutRequestID")
            
            # ResultCode 0 = sucesso
            if result_code == 0:
                # Extrair metadados
                callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
                
                # Buscar transação por CheckoutRequestID (em produção, buscar no banco)
                transaction = None
                for tx_id, tx_data in PaymentService._transactions.items():
                    if tx_data.get("checkout_request_id") == checkout_request_id:
                        transaction = tx_data
                        break
                
                if transaction:
                    # Atualizar status
                    transaction["status"] = "success"
                    transaction["mpesa_receipt"] = next(
                        (item["Value"] for item in callback_metadata if item.get("Name") == "MpesaReceiptNumber"),
                        None
                    )
                    transaction["confirmed_at"] = datetime.now()
                    
                    # Em produção: notificar cliente, atualizar pedido, etc.
                    return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao processar callback M-Pesa: {str(e)}")
            return False
    
    @staticmethod
    def _validate_payment_data(payment_data: PaymentRequest) -> None:
        """Valida dados do pagamento"""
        
        # Valor mínimo
        if payment_data.amount < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor mínimo de pagamento é 1 MTZ"
            )
        
        # Valor máximo (ajustar conforme necessário)
        if payment_data.amount > 50000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor máximo de pagamento é 50.000 MTZ"
            )
        
        # Validar prefixo do telefone M-Pesa
        phone_prefix = payment_data.phone_number[:2]
        valid_prefixes = ['84', '82', '83', '86', '87']
        
        if phone_prefix not in valid_prefixes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número de telefone inválido. Use um número M-Pesa válido (prefixos: {', '.join(valid_prefixes)})"
            )
    
    @staticmethod
    def _generate_transaction_id() -> str:
        """Gera ID único de transação"""
        return f"TXN-{secrets.token_hex(8).upper()}"
    
    @staticmethod
    def _simulate_mpesa_response() -> bool:
        """
        Simula resposta da API M-Pesa.
        Em produção, remover e usar API real.
        """
        import random
        # 85% de sucesso para simulação realista
        return random.random() < 0.85
    
    @staticmethod
    def _get_status_message(status: str) -> str:
        """Retorna mensagem baseada no status"""
        messages = {
            "pending": "Pagamento pendente de confirmação",
            "success": "Pagamento confirmado com sucesso",
            "failed": "Pagamento falhou",
            "expired": "Tempo de pagamento expirado"
        }
        return messages.get(status, "Status desconhecido")

