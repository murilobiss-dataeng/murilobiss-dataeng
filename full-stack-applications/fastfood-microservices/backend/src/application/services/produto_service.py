from uuid import uuid4
import logging

from src.adapters.input.dto.produto_dto import ProdutoCreate, ProdutoResponse
from src.domain.models.produto import Produto
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort
from src.ports.services.produto_service_port import ProdutoServicePort

# Configure logging
logger = logging.getLogger(__name__)

class ProdutoService(ProdutoServicePort):
    def __init__(self, produto_repository: ProdutoRepositoryPort):
        self.produto_repository = produto_repository

    def criar_produto(self, produto_create: ProdutoCreate) -> ProdutoResponse:
        try:
            produto = Produto(
                id=uuid4(),
                nome=produto_create.nome,
                categoria=produto_create.categoria,
                preco=produto_create.preco
            )
            self.produto_repository.salvar(produto)
            return ProdutoResponse(**produto.__dict__)
        except Exception as e:
            logger.error(f"Erro ao criar produto: {e}")
            raise

    def listar_produtos(self) -> list[ProdutoResponse]:
        try:
            logger.info("Service: Iniciando listagem de produtos...")
            produtos = self.produto_repository.listar()
            logger.info(f"Service: Produtos obtidos do repository: {len(produtos)}")
            
            response_list = [ProdutoResponse(**p.__dict__) for p in produtos]
            logger.info(f"Service: Produtos convertidos para response: {len(response_list)}")
            
            return response_list
        except Exception as e:
            logger.error(f"Erro ao listar produtos no service: {e}")
            raise

    def buscar_produto(self, produto_id: str) -> ProdutoResponse | None:
        try:
            produto = self.produto_repository.buscar_por_id(produto_id)
            if produto:
                return ProdutoResponse(**produto.__dict__)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar produto {produto_id}: {e}")
            raise

    def buscar_por_categoria(self, categoria: str) -> list[ProdutoResponse]:
        try:
            produtos = self.produto_repository.buscar_por_categoria(categoria)
            return [ProdutoResponse(**p.__dict__) for p in produtos]
        except Exception as e:
            logger.error(f"Erro ao buscar produtos por categoria {categoria}: {e}")
            raise

    def deletar_produto(self, produto_id: str) -> None:
        try:
            self.produto_repository.deletar(produto_id)
        except Exception as e:
            logger.error(f"Erro ao deletar produto {produto_id}: {e}")
            raise
