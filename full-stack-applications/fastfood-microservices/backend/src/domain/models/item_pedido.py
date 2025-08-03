from dataclasses import dataclass
from uuid import UUID


@dataclass
class ItemPedido:
    produto_id: UUID
    quantidade: int

