from abc import ABC, abstractmethod
from uuid import UUID

from src.adapters.input.dto.pedido_dto import PedidoCreate, PedidoResponse, ItemPedidoDTO
from src.domain.models.pedido import StatusPedido


class PedidoServicePort(ABC):
    @abstractmethod
    def criar_pedido(self, pedido_create: PedidoCreate) -> PedidoResponse:
        pass

    @abstractmethod
    def buscar_pedido_por_id(self, pedido_id: UUID) -> PedidoResponse | None:
        pass

    @abstractmethod
    def listar_pedidos(self) -> list[PedidoResponse]:
        pass

    @abstractmethod
    def listar_pedidos_ordenados(self) -> list[PedidoResponse]:
        pass

    @abstractmethod
    def deletar_pedido(self, pedido_id: UUID) -> None:
        pass

    @abstractmethod
    def buscar_pedidos_por_cliente(self, cliente_id: UUID) -> list[PedidoResponse]:
        pass

    @abstractmethod
    def atualizar_status_pedido(self, pedido_id: UUID, novo_status: StatusPedido) -> PedidoResponse:
        pass

    @abstractmethod
    def cancelar_pedido(self, pedido_id: UUID) -> PedidoResponse:
        pass

    @abstractmethod
    def adicionar_item_ao_pedido(self, pedido_id: UUID, item: ItemPedidoDTO) -> PedidoResponse:
        pass
