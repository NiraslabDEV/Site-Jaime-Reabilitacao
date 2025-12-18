"""
Cliente M-Pesa para integração com API de Link de Pagamentos
"""
import requests
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings
from fastapi import HTTPException, status


class MpesaClient:
    """Cliente para comunicação com API M-Pesa"""
    
    _access_token: Optional[str] = None
    _token_expires_at: Optional[datetime] = None
    
    @classmethod
    async def get_access_token(cls) -> str:
        """
        Obtém ou renova o access token da API M-Pesa.
        Token expira em 1 hora conforme configuração.
        """
        
        # Verificar se token ainda é válido (com margem de 5 minutos)
        if cls._access_token and cls._token_expires_at:
            if datetime.now() < cls._token_expires_at - timedelta(minutes=5):
                return cls._access_token
        
        # Obter novo token
        try:
            # URL de autenticação (ajustar conforme documentação da API)
            auth_url = f"{settings.MPESA_API_URL}/oauth/v1/generate?grant_type=client_credentials"
            
            # Criar credenciais básicas (API Key como username, sem password ou vice-versa)
            # Ajustar conforme especificação da API
            api_key = settings.MPESA_API_KEY
            
            # Autenticação básica (ajustar conforme necessário)
            # Algumas APIs usam API Key no header, outras em Basic Auth
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Alternativa: Basic Auth se necessário
            # credentials = base64.b64encode(f"{api_key}:".encode()).decode()
            # headers = {
            #     "Authorization": f"Basic {credentials}",
            #     "Content-Type": "application/json"
            # }
            
            response = requests.get(auth_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cls._access_token = data.get("access_token")
                
                # Calcular expiração (1 hora conforme configuração)
                expires_in = data.get("expires_in", 3600)
                cls._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                return cls._access_token
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Erro ao obter token M-Pesa: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro ao conectar com API M-Pesa: {str(e)}"
            )
    
    @classmethod
    async def initiate_payment_link(
        cls,
        phone_number: str,
        amount: float,
        order_reference: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inicia um link de pagamento M-Pesa.
        
        Args:
            phone_number: Número de telefone (formato: 258XXXXXXXX)
            amount: Valor do pagamento
            order_reference: Referência única do pedido
            description: Descrição do pagamento
        
        Returns:
            Dicionário com dados da transação
        """
        
        # Obter token de acesso
        access_token = await cls.get_access_token()
        
        # Preparar dados do pagamento
        payment_data = {
            "phoneNumber": phone_number,
            "amount": str(int(amount)),  # Converter para string e remover decimais
            "accountReference": order_reference,
            "transactionDesc": description or f"Pagamento pedido {order_reference}",
            "callbackUrl": settings.MPESA_CALLBACK_URL or f"{settings.MPESA_API_URL}/api/payment/callback"
        }
        
        # URL do endpoint de pagamento (ajustar conforme documentação)
        payment_url = f"{settings.MPESA_API_URL}/mpesa/payment/v1/processrequest"
        
        # Headers com token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                payment_url,
                json=payment_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get("errorMessage", error_data.get("message", error_msg))
                except:
                    pass
                
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao processar pagamento M-Pesa: {error_msg}"
                )
                
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro ao conectar com API M-Pesa: {str(e)}"
            )
    
    @classmethod
    async def check_payment_status(
        cls,
        transaction_id: str
    ) -> Dict[str, Any]:
        """
        Consulta o status de uma transação.
        
        Args:
            transaction_id: ID da transação
        
        Returns:
            Status da transação
        """
        
        access_token = await cls.get_access_token()
        
        # URL de consulta (ajustar conforme documentação)
        status_url = f"{settings.MPESA_API_URL}/mpesa/payment/v1/queryrequest"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        query_data = {
            "transactionId": transaction_id
        }
        
        try:
            response = requests.post(
                status_url,
                json=query_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao consultar status: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro ao conectar com API M-Pesa: {str(e)}"
            )





