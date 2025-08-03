import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.db.session import Base


class PagamentoModel(Base):
    __tablename__ = "tb_pagamentos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("tb_pedidos.id"), nullable=False)
    status = Column(String, default="pendente", nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(UTC))
    data_confirmacao = Column(DateTime, nullable=True)
    pedido = relationship("PedidoModel", back_populates="pagamento")


