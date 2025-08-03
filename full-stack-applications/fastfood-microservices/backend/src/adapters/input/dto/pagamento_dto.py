from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class PagamentoQRCodeResponse(BaseModel):
    status: str
    qrcode_url: str
    qrcode_id: str


class StatusPagamentoResponse(BaseModel):
    pedido_id: UUID
    status: str
    data_criacao: datetime
    data_confirmacao: datetime | None = None


class WebhookPagamentoDTO(BaseModel):
    pedido_id: UUID
    status: str  # "approved", "rejected", "pending"
    external_reference: str | None = None
    payment_id: str | None = None
    data_processamento: datetime | None = None
