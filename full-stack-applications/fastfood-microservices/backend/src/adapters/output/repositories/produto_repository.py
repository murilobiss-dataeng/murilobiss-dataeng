from decimal import Decimal
import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.models.produto import Produto
from src.infrastructure.db.models.produto_model import ProdutoModel
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort

# Configure logging
logger = logging.getLogger(__name__)

class ProdutoRepository(ProdutoRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        try:
            model = self.db.query(ProdutoModel).filter_by(id=produto_id).first()
            return self._to_domain(model) if model else None
        except Exception as e:
            logger.error(f"Erro ao buscar produto por ID {produto_id}: {e}")
            raise

    def listar(self) -> list[Produto]:
        try:
            logger.info("Iniciando listagem de produtos...")
            models = self.db.query(ProdutoModel).all()
            logger.info(f"Produtos encontrados no banco: {len(models)}")
            
            produtos = [self._to_domain(m) for m in models]
            logger.info(f"Produtos convertidos para domínio: {len(produtos)}")
            
            return produtos
        except Exception as e:
            logger.error(f"Erro ao listar produtos: {e}")
            raise

    def salvar(self, produto: Produto) -> Produto:
        try:
            model = ProdutoModel(
                nome=produto.nome,
                categoria=produto.categoria,
                preco=float(produto.preco),
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            produto.id = model.id
            return self._to_domain(model)
        except Exception as e:
            logger.error(f"Erro ao salvar produto: {e}")
            self.db.rollback()
            raise

    def deletar(self, produto_id: int) -> None:
        try:
            model = self.db.query(ProdutoModel).filter_by(id=produto_id).first()
            if not model:
                raise ValueError("Produto não encontrado")
            self.db.delete(model)
            self.db.commit()
        except Exception as e:
            logger.error(f"Erro ao deletar produto {produto_id}: {e}")
            self.db.rollback()
            raise

    def buscar_por_categoria(self, categoria: str) -> list[Produto]:
        try:
            models = self.db.query(ProdutoModel).filter_by(categoria=categoria).all()
            return [self._to_domain(m) for m in models]
        except Exception as e:
            logger.error(f"Erro ao buscar produtos por categoria {categoria}: {e}")
            raise

    def _to_domain(self, model: ProdutoModel) -> Produto:
        try:
            return Produto(
                id=model.id,
                nome=model.nome,
                categoria=model.categoria,
                preco=Decimal(str(model.preco)),
                estoque=100  # Estoque padrão para produtos existentes
            )
        except Exception as e:
            logger.error(f"Erro ao converter modelo para domínio: {e}")
            raise
