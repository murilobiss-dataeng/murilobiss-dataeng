from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.db.session import Base


class ItemPedidoModel(Base):
    __tablename__ = "tb_itens_pedido"
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("tb_pedidos.id"), primary_key=True)
    produto_id = Column(UUID(as_uuid=True), ForeignKey("tb_produtos.id"), primary_key=True)
    quantidade = Column(Integer, nullable=False)
    pedido = relationship("PedidoModel", back_populates="itens")
