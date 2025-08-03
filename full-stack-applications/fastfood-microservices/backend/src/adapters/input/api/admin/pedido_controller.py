from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import (
    get_fila_repository,
    get_pedido_repository,
    get_pedido_service,
)
from src.adapters.input.dto.pedido_dto import AtualizarStatusPedidoDTO, PedidoResponse
from src.application.services.pedido_service import PedidoService
from src.ports.repositories.fila_pedidos_repository_port import (
    FilaPedidosRepositoryPort,
)
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.adapters.input.api.security.jwt_handler import get_current_admin 

router = APIRouter(prefix="/v1/api/admin/pedidos", tags=["Painel administrativo de Pedidos"], dependencies=[Depends(get_current_admin)])

@router.get("/", response_model=list[PedidoResponse], summary="Listar todos os pedidos ordenados")
def listar_pedidos_ordenados(service: PedidoService = Depends(get_pedido_service)):
    """Lista pedidos ordenados por: Pronto > Em Preparação > Recebido, e por data (mais antigos primeiro)"""
    return service.listar_pedidos_ordenados()

@router.get("/em-aberto", response_model=list[PedidoResponse], summary="Listar pedidos em aberto")
def listar_pedidos_em_aberto(
    fila_repo: FilaPedidosRepositoryPort = Depends(get_fila_repository),
    pedido_repo: PedidoRepositoryPort = Depends(get_pedido_repository),
):
    """Lista pedidos em aberto (não finalizados)"""
    fila = fila_repo.listar_em_aberto()
    pedidos = []
    for f in fila:
        pedido = pedido_repo.buscar_por_id(f.id)
        if pedido:
            pedidos.append(pedido)
    return pedidos

@router.patch("/{pedido_id}/status", response_model=PedidoResponse, summary="Atualizar status do pedido")
def atualizar_status_pedido(
    pedido_id: UUID,
    dto: AtualizarStatusPedidoDTO,
    service: PedidoService = Depends(get_pedido_service),
):
    """Atualiza o status do pedido para a cozinha"""
    return service.atualizar_status_pedido(pedido_id, dto.status)

@router.delete("/{pedido_id}", status_code=204, summary="Deletar pedido")
def deletar_pedido(pedido_id: UUID, service: PedidoService = Depends(get_pedido_service)):
    """Deleta um pedido específico"""
    service.deletar_pedido(pedido_id)
