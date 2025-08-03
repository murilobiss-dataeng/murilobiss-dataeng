from uuid import UUID

from fastapi import HTTPException

from src.adapters.input.dto.pedido_dto import (
    ItemPedidoDTO,
    PedidoCreate,
    PedidoResponse,
)
from src.domain.models.pedido import ItemPedido, Pedido, StatusPedido
from src.ports.repositories.fila_pedidos_repository_port import (
    FilaPedidosRepositoryPort,
)
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort
from src.ports.services.pedido_service_port import PedidoServicePort


class PedidoService(PedidoServicePort):
    def __init__(
        self,
        repository: PedidoRepositoryPort,
        fila_repository: FilaPedidosRepositoryPort,
        produto_repository: ProdutoRepositoryPort,
        cliente_repository: ClienteRepositoryPort,
    ):
        self.repository = repository
        self.fila_repository = fila_repository
        self.produto_repository = produto_repository
        self.cliente_repository = cliente_repository

    def criar_pedido(self, pedido_create: PedidoCreate) -> PedidoResponse:
        """Cria um novo pedido com validações de domínio"""
        # Validar cliente
        if pedido_create.cliente_id:
            cliente = self.cliente_repository.buscar_por_id(pedido_create.cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            if not cliente.pode_fazer_pedido():
                raise HTTPException(status_code=403, detail="Cliente inativo")

        # Validar produtos e estoque
        itens_validados = []
        for item_dto in pedido_create.itens:
            produto = self.produto_repository.buscar_por_id(item_dto.produto_id)
            if not produto:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Produto {item_dto.produto_id} não encontrado"
                )
            
            if not produto.esta_disponivel(item_dto.quantidade):
                raise HTTPException(
                    status_code=422,
                    detail=f"Estoque insuficiente para {produto.nome}"
                )
            
            # Reservar estoque
            if not produto.reservar_estoque(item_dto.quantidade):
                raise HTTPException(
                    status_code=422,
                    detail=f"Falha ao reservar estoque para {produto.nome}"
                )
            
            itens_validados.append(
                ItemPedido(produto_id=item_dto.produto_id, quantidade=item_dto.quantidade)
            )

        try:
            # Criar pedido com validações de domínio
            pedido = Pedido.criar(
                cliente_id=pedido_create.cliente_id, 
                itens=itens_validados
            )
            
            # Salvar pedido
            pedido = self.repository.salvar(pedido)
            self.fila_repository.enfileirar(pedido.id)

            return self._to_response(pedido)
            
        except ValueError as e:
            # Liberar estoque em caso de erro
            for item in itens_validados:
                produto = self.produto_repository.buscar_por_id(item.produto_id)
                if produto:
                    produto.liberar_estoque(item.quantidade)
            raise HTTPException(status_code=422, detail=str(e))

    def buscar_pedido_por_id(self, pedido_id: UUID) -> PedidoResponse:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return self._to_response(pedido)

    def listar_pedidos(self) -> list[PedidoResponse]:
        pedidos = self.repository.listar()
        return [self._to_response(p) for p in pedidos]

    def listar_pedidos_ordenados(self) -> list[PedidoResponse]:
        """Lista pedidos ordenados conforme regras da Fase 2:
        1. Pronto > Em Preparação > Recebido
        2. Pedidos mais antigos primeiro
        3. Pedidos com status Finalizado não aparecem
        """
        pedidos = self.repository.listar_ordenados()
        return [self._to_response(p) for p in pedidos]

    def deletar_pedido(self, pedido_id: UUID) -> None:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        # Liberar estoque
        for item in pedido.itens:
            produto = self.produto_repository.buscar_por_id(item.produto_id)
            if produto:
                produto.liberar_estoque(item.quantidade)
        
        self.repository.deletar(pedido_id)

    def buscar_pedidos_por_cliente(self, cliente_id: UUID) -> list[PedidoResponse]:
        cliente = self.cliente_repository.buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        pedidos = self.repository.buscar_por_cliente(cliente_id)
        return [self._to_response(p) for p in pedidos]

    def atualizar_status_pedido(self, pedido_id: UUID, novo_status: StatusPedido) -> PedidoResponse:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        try:
            # Atualizar status com validações de domínio
            pedido.atualizar_status(novo_status)
            pedido = self.repository.salvar(pedido)
            
            # Atualizar fila de pedidos
            self.fila_repository.atualizar_status(pedido_id, novo_status.value)
            
            return self._to_response(pedido)
            
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    def cancelar_pedido(self, pedido_id: UUID) -> PedidoResponse:
        """Cancela um pedido com validações"""
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        try:
            # Cancelar pedido com validações de domínio
            pedido.cancelar()
            pedido = self.repository.salvar(pedido)
            
            # Liberar estoque
            for item in pedido.itens:
                produto = self.produto_repository.buscar_por_id(item.produto_id)
                if produto:
                    produto.liberar_estoque(item.quantidade)
            
            # Atualizar fila
            self.fila_repository.atualizar_status(pedido_id, StatusPedido.FINALIZADO.value)
            
            return self._to_response(pedido)
            
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    def adicionar_item_ao_pedido(self, pedido_id: UUID, item: ItemPedidoDTO) -> PedidoResponse:
        """Adiciona um item a um pedido existente"""
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        # Validar produto
        produto = self.produto_repository.buscar_por_id(item.produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        if not produto.esta_disponivel(item.quantidade):
            raise HTTPException(status_code=422, detail="Estoque insuficiente")
        
        try:
            # Adicionar item com validações de domínio
            novo_item = ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            pedido.adicionar_item(novo_item)
            
            # Reservar estoque
            produto.reservar_estoque(item.quantidade)
            
            pedido = self.repository.salvar(pedido)
            return self._to_response(pedido)
            
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    def _to_response(self, pedido: Pedido) -> PedidoResponse:
        return PedidoResponse(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            status=pedido.status,
            data_criacao=pedido.data_criacao,
            itens=[
                ItemPedidoDTO(produto_id=item.produto_id, quantidade=item.quantidade)
                for item in pedido.itens
            ],
        )
