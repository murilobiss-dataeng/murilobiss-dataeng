from abc import ABC, abstractmethod

from src.domain.models.cliente import Cliente


class ClienteRepositoryPort(ABC):
    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Cliente | None:
        pass

    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def listar(self) -> list[Cliente]:
        pass

