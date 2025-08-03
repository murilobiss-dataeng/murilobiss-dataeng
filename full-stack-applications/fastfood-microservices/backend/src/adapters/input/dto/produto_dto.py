from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    preco: Decimal

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: UUID
