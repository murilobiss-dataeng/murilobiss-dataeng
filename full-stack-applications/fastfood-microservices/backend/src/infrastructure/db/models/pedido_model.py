import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.db.session import Base


class PedidoModel(Base):
    __tablename__ = "tb_pedidos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("tb_clientes.id"), nullable=False)
    status = Column(String, default="pendente", nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(UTC))
    itens = relationship("ItemPedidoModel", back_populates="pedido")
    pagamento = relationship("PagamentoModel", back_populates="pedido", uselist=False)


