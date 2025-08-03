import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.session import Base


class ClienteModel(Base):
    __tablename__ = "tb_clientes"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nome = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)

