import uuid

from sqlalchemy import Column, Float, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.session import Base


class ProdutoModel(Base):
    __tablename__ = "tb_produtos"
    __table_args__ = (UniqueConstraint('nome', name='uq_produto_nome'),)
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

