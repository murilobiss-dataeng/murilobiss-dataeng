from uuid import UUID, uuid4
from datetime import UTC, datetime

from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse, StatusPagamentoResponse, WebhookPagamentoDTO
from src.domain.models.pedido import StatusPedido
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.ports.repositories.pagamento_repository_port import PagamentoRepositoryPort
from src.ports.services.pagamento_service_port import PagamentoServicePort


class PagamentoService(PagamentoServicePort):
    def __init__(
        self,
        pedido_repository: PedidoRepositoryPort,
        pagamento_repository: PagamentoRepositoryPort
    ):
        self.pedido_repository = pedido_repository
        self.pagamento_repository = pagamento_repository

    def gerar_qrcode(self) -> PagamentoQRCodeResponse:
        """Gera QRCode para pagamento (mock do Mercado Pago)"""
        qrcode_id = str(uuid4())
        return PagamentoQRCodeResponse(
            status="ok",
            qrcode_url=f"https://mercadopago.com/qrcode/{qrcode_id}",
            qrcode_id=qrcode_id
        )

    def consultar_status_pagamento(self, pedido_id: UUID) -> StatusPagamentoResponse:
        """Consulta o status de pagamento de um pedido"""
        pagamento = self.pagamento_repository.buscar_por_pedido_id(pedido_id)
        if not pagamento:
            raise Exception("Pagamento não encontrado para este pedido")
        
        return StatusPagamentoResponse(
            pedido_id=pagamento.pedido_id,
            status=pagamento.status,
            data_criacao=pagamento.data_criacao,
            data_confirmacao=pagamento.data_confirmacao
        )

    def processar_webhook(self, webhook_data: WebhookPagamentoDTO) -> dict:
        """Processa webhook de confirmação de pagamento"""
        # Buscar pagamento existente ou criar novo
        pagamento = self.pagamento_repository.buscar_por_pedido_id(webhook_data.pedido_id)
        
        if not pagamento:
            raise Exception("Pedido não encontrado")
        
        # Atualizar status do pagamento
        pagamento.status = webhook_data.status
        if webhook_data.status == "approved":
            pagamento.data_confirmacao = datetime.now(UTC)
            # Atualizar status do pedido para "Em preparação"
            pedido = self.pedido_repository.buscar_por_id(webhook_data.pedido_id)
            if pedido:
                pedido.status = StatusPedido.PREPARANDO
                self.pedido_repository.salvar(pedido)
        
        self.pagamento_repository.salvar(pagamento)
        
        return {
            "status": "success",
            "message": f"Pagamento {webhook_data.status} processado com sucesso",
            "pedido_id": str(webhook_data.pedido_id)
        }

    def confirmar_pagamento(self, pedido_id: UUID):
        """Confirma pagamento manualmente (para testes)"""
        pedido = self.pedido_repository.buscar_por_id(pedido_id)
        if not pedido:
            raise Exception("Pedido não encontrado")

        pedido.status = StatusPedido.PAGO
        self.pedido_repository.salvar(pedido)
        return pedido
