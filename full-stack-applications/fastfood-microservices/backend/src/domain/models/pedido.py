from datetime import UTC, datetime
from uuid import UUID, uuid4
from typing import List

from src.domain.models.item_pedido import ItemPedido
from src.domain.models.status_pedido import StatusPedido


class Pedido:
    def __init__(
        self,
        id: UUID,
        cliente_id: UUID | None,
        status: StatusPedido = StatusPedido.RECEBIDO,
        data_criacao: datetime | None = None,
        itens: list[ItemPedido] | None = None,
        observacoes: str | None = None,
    ):
        self.id = id
        self.cliente_id = cliente_id
        self.status = status
        self.data_criacao = data_criacao or datetime.now(UTC)
        self.itens = itens or []
        self.observacoes = observacoes
        
        # Validações de domínio
        self._validar_pedido()

    @classmethod
    def criar(cls, cliente_id: UUID, itens: list["ItemPedido"], observacoes: str | None = None) -> "Pedido":
        """Factory method para criar um novo pedido com validações"""
        if not itens:
            raise ValueError("Pedido deve ter pelo menos um item")
        
        if len(itens) > 20:
            raise ValueError("Pedido não pode ter mais de 20 itens")
        
        # Validar quantidade de cada item
        for item in itens:
            if item.quantidade <= 0:
                raise ValueError(f"Quantidade do item deve ser maior que zero")
            if item.quantidade > 50:
                raise ValueError(f"Quantidade máxima por item é 50")
        
        return cls(
            id=uuid4(),
            cliente_id=cliente_id,
            status=StatusPedido.RECEBIDO,
            data_criacao=datetime.now(UTC),
            itens=itens,
            observacoes=observacoes,
        )

    def adicionar_item(self, item: ItemPedido) -> None:
        """Adiciona um item ao pedido com validações"""
        if self.status in [StatusPedido.FINALIZADO, StatusPedido.PRONTO]:
            raise ValueError("Não é possível adicionar itens a um pedido finalizado ou pronto")
        
        if len(self.itens) >= 20:
            raise ValueError("Pedido já possui o máximo de itens permitidos")
        
        # Verificar se o item já existe e somar quantidades
        for item_existente in self.itens:
            if item_existente.produto_id == item.produto_id:
                nova_quantidade = item_existente.quantidade + item.quantidade
                if nova_quantidade > 50:
                    raise ValueError(f"Quantidade total do produto não pode exceder 50")
                item_existente.quantidade = nova_quantidade
                return
        
        self.itens.append(item)

    def remover_item(self, produto_id: UUID) -> None:
        """Remove um item do pedido"""
        if self.status in [StatusPedido.FINALIZADO, StatusPedido.PRONTO]:
            raise ValueError("Não é possível remover itens de um pedido finalizado ou pronto")
        
        self.itens = [item for item in self.itens if item.produto_id != produto_id]

    def atualizar_status(self, novo_status: StatusPedido) -> None:
        """Atualiza o status do pedido com validações de transição"""
        transicoes_validas = {
            StatusPedido.RECEBIDO: [StatusPedido.PAGO, StatusPedido.PREPARANDO],
            StatusPedido.PAGO: [StatusPedido.PREPARANDO],
            StatusPedido.PREPARANDO: [StatusPedido.PRONTO],
            StatusPedido.PRONTO: [StatusPedido.FINALIZADO],
            StatusPedido.FINALIZADO: []
        }
        
        if novo_status not in transicoes_validas.get(self.status, []):
            raise ValueError(f"Transição de status inválida: {self.status} -> {novo_status}")
        
        self.status = novo_status

    def calcular_total(self) -> float:
        """Calcula o total do pedido"""
        # Esta implementação seria expandida com os preços dos produtos
        return sum(item.quantidade for item in self.itens) * 10.0  # Mock

    def pode_ser_cancelado(self) -> bool:
        """Verifica se o pedido pode ser cancelado"""
        return self.status in [StatusPedido.RECEBIDO, StatusPedido.PAGO]

    def cancelar(self) -> None:
        """Cancela o pedido"""
        if not self.pode_ser_cancelado():
            raise ValueError("Pedido não pode ser cancelado no status atual")
        
        self.status = StatusPedido.FINALIZADO

    def _validar_pedido(self) -> None:
        """Validações internas do pedido"""
        if not self.itens:
            raise ValueError("Pedido deve ter pelo menos um item")
        
        if len(self.itens) > 20:
            raise ValueError("Pedido não pode ter mais de 20 itens")
        
        # Validar que não há produtos duplicados
        produtos_ids = [item.produto_id for item in self.itens]
        if len(produtos_ids) != len(set(produtos_ids)):
            raise ValueError("Pedido não pode ter produtos duplicados")

    def __str__(self) -> str:
        return f"Pedido {self.id} - Status: {self.status} - Itens: {len(self.itens)}"

    def __repr__(self) -> str:
        return f"Pedido(id={self.id}, status={self.status}, itens={len(self.itens)})"
