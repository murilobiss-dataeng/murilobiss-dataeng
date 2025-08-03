from abc import ABC, abstractmethod

from src.domain.models.produto import Produto


class ProdutoRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def listar(self) -> list[Produto]:
        pass

    @abstractmethod
    def buscar_por_id(self, produto_id: str) -> Produto | None:
        pass

    @abstractmethod
    def deletar(self, produto_id: str) -> None:
        pass

    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> list[Produto]:
        pass
