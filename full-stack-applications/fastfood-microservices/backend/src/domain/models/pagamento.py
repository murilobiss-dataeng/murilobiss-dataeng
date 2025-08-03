from datetime import UTC, datetime
from uuid import UUID, uuid4


class Pagamento:
    def __init__(
        self,
        id: UUID,
        pedido_id: UUID,
        status: str = "pending",
        data_criacao: datetime | None = None,
        data_confirmacao: datetime | None = None,
    ):
        self.id = id
        self.pedido_id = pedido_id
        self.status = status
        self.data_criacao = data_criacao or datetime.now(UTC)
        self.data_confirmacao = data_confirmacao

    @classmethod
    def criar(cls, pedido_id: UUID, status: str = "pending") -> "Pagamento":
        return cls(
            id=uuid4(),
            pedido_id=pedido_id,
            status=status,
            data_criacao=datetime.now(UTC),
        ) 