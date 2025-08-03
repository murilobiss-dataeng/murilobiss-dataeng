from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.pedido import Pedido


class PedidoRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def listar(self) -> list[Pedido]:
        pass

    @abstractmethod
    def listar_ordenados(self) -> list[Pedido]:
        pass

    @abstractmethod
    def buscar_por_id(self, pedido_id: UUID) -> Pedido | None:
        pass

    @abstractmethod
    def deletar(self, pedido_id: UUID) -> None:
        pass

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: UUID) -> list[Pedido]:
        pass

    @abstractmethod
    def atualizar_status(self, pedido_id: UUID, status: str) -> Pedido:
        pass
