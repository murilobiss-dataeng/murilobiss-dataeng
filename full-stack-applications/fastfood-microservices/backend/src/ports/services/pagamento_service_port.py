from abc import ABC, abstractmethod
from uuid import UUID

from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse, StatusPagamentoResponse, WebhookPagamentoDTO


class PagamentoServicePort(ABC):
    @abstractmethod
    def gerar_qrcode(self) -> PagamentoQRCodeResponse:
        pass

    @abstractmethod
    def consultar_status_pagamento(self, pedido_id: UUID) -> StatusPagamentoResponse:
        pass

    @abstractmethod
    def processar_webhook(self, webhook_data: WebhookPagamentoDTO) -> dict:
        pass

    @abstractmethod
    def confirmar_pagamento(self, pedido_id: UUID):
        pass
