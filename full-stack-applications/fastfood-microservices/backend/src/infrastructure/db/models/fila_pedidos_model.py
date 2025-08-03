import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.session import Base


class FilaPedidosModel(Base):
    __tablename__ = "tb_fila_pedidos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    status = Column(String, default="pendente", nullable=False)
    payload = Column(String, nullable=True)
