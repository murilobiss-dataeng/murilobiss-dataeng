from abc import ABC, abstractmethod

from src.adapters.input.dto.produto_dto import ProdutoCreate, ProdutoResponse


class ProdutoServicePort(ABC):
    @abstractmethod
    def criar_produto(self, produto_create: ProdutoCreate) -> ProdutoResponse:
        pass

    @abstractmethod
    def listar_produtos(self) -> list[ProdutoResponse]:
        pass

    @abstractmethod
    def buscar_produto(self, produto_id: str) -> ProdutoResponse | None:
        pass

    @abstractmethod
    def deletar_produto(self, produto_id: str) -> None:
        pass

    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> list[ProdutoResponse]:
        pass
