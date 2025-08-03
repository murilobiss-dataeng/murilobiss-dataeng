from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.pagamento import Pagamento


class PagamentoRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, pagamento: Pagamento) -> Pagamento:
        pass

    @abstractmethod
    def buscar_por_pedido_id(self, pedido_id: UUID) -> Pagamento | None:
        pass

    @abstractmethod
    def buscar_por_id(self, pagamento_id: UUID) -> Pagamento | None:
        pass

    @abstractmethod
    def listar(self) -> list[Pagamento]:
        pass 