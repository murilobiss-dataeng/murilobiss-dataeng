from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.models.pagamento import Pagamento
from src.infrastructure.db.models.pagamento_model import PagamentoModel
from src.ports.repositories.pagamento_repository_port import PagamentoRepositoryPort


class PagamentoRepository(PagamentoRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pagamento: Pagamento) -> Pagamento:
        pagamento_model = self.db.query(PagamentoModel).filter_by(id=pagamento.id).first()

        if not pagamento_model:
            pagamento_model = PagamentoModel(
                id=pagamento.id,
                pedido_id=pagamento.pedido_id,
                status=pagamento.status,
                data_criacao=pagamento.data_criacao,
                data_confirmacao=pagamento.data_confirmacao,
            )
            self.db.add(pagamento_model)
        else:
            pagamento_model.status = pagamento.status
            pagamento_model.data_confirmacao = pagamento.data_confirmacao

        self.db.commit()
        self.db.refresh(pagamento_model)
        return self._converter_para_entidade(pagamento_model)

    def buscar_por_pedido_id(self, pedido_id: UUID) -> Pagamento | None:
        model = self.db.query(PagamentoModel).filter_by(pedido_id=pedido_id).first()
        if model:
            return self._converter_para_entidade(model)
        return None

    def buscar_por_id(self, pagamento_id: UUID) -> Pagamento | None:
        model = self.db.query(PagamentoModel).filter_by(id=pagamento_id).first()
        if model:
            return self._converter_para_entidade(model)
        return None

    def listar(self) -> list[Pagamento]:
        pagamentos_model = self.db.query(PagamentoModel).all()
        return [self._converter_para_entidade(p) for p in pagamentos_model]

    def _converter_para_entidade(self, model: PagamentoModel) -> Pagamento:
        return Pagamento(
            id=model.id,
            pedido_id=model.pedido_id,
            status=model.status,
            data_criacao=model.data_criacao,
            data_confirmacao=model.data_confirmacao,
        ) 