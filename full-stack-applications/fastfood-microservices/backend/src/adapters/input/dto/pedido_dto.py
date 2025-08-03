from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.models.pedido import StatusPedido


class ItemPedidoDTO(BaseModel):
    produto_id: UUID
    quantidade: int


class CheckoutPedidoDTO(BaseModel):
    cliente_id: UUID | None = None
    itens: list[ItemPedidoDTO]
    observacoes: str | None = None


class PedidoCreate(BaseModel):
    cliente_id: UUID
    itens: list[ItemPedidoDTO]


class PedidoResponse(BaseModel):
    id: UUID
    cliente_id: UUID
    status: StatusPedido
    data_criacao: datetime
    itens: list[ItemPedidoDTO]


class AtualizarStatusPedidoDTO(BaseModel):
    status: StatusPedido
