from enum import Enum


class StatusPedido(str, Enum):
    RECEBIDO = "Recebido"
    PAGO = "Pago"
    PREPARANDO = "Em preparação"
    PRONTO = "Pronto"
    FINALIZADO = "Finalizado"
