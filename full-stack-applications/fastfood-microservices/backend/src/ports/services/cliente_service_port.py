from abc import ABC, abstractmethod

from src.adapters.input.dto.cliente_dto import ClienteCreate, ClienteResponse


class ClienteServicePort(ABC):

    @abstractmethod
    def criar_ou_obter_cliente(self, cliente_create: ClienteCreate) -> ClienteResponse:
        pass

    @abstractmethod
    def buscar_cliente_por_cpf(self, cpf: str) -> ClienteResponse | None:
        pass

    @abstractmethod
    def listar_clientes(self) -> list[ClienteResponse]:
        pass
