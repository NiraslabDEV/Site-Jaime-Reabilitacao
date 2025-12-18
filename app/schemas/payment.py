"""
Schemas para pagamento M-Pesa
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class PaymentRequest(BaseModel):
    """Schema para requisição de pagamento"""
    amount: float = Field(..., gt=0, description="Valor total do pagamento")
    phone_number: str = Field(..., min_length=9, max_length=9, description="Número de telefone (9 dígitos)")
    order_reference: str = Field(..., description="Referência única do pedido")

    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Valida que o número contém apenas dígitos"""
        if not v.isdigit():
            raise ValueError('O número de telefone deve conter apenas dígitos')
        return v

    @validator('amount')
    def validate_amount(cls, v):
        """Valida que o valor é positivo"""
        if v <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return round(v, 2)

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 450.00,
                "phone_number": "841234567",
                "order_reference": "ORD-ABC123"
            }
        }


class PaymentResponse(BaseModel):
    """Schema para resposta de pagamento"""
    success: bool
    message: str
    transaction_id: Optional[str] = None
    order_reference: str
    amount: float
    phone_number: str
    status: str = Field(..., description="Status do pagamento: pending, success, failed")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Pagamento iniciado. Confirme no seu telefone.",
                "transaction_id": "TXN-123456789",
                "order_reference": "ORD-ABC123",
                "amount": 450.00,
                "phone_number": "841234567",
                "status": "pending",
                "timestamp": "2024-01-01T12:00:00"
            }
        }





