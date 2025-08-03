from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_cliente_service
from src.adapters.input.dto.cliente_dto import ClienteResponse
from src.ports.services.cliente_service_port import ClienteServicePort
from src.adapters.input.api.security.jwt_handler import get_current_admin 

router = APIRouter(prefix="/v1/api/admin/clientes", tags=["Painel administrativo de Clientes"], dependencies=[Depends(get_current_admin)])

@router.get("/", response_model=list[ClienteResponse], summary="Listar todos os clientes")
def listar_clientes(service: ClienteServicePort = Depends(get_cliente_service)):
    return service.listar_clientes()

@router.get("/{cpf}", response_model=ClienteResponse, summary="Buscar cliente por CPF")
def buscar_cliente_por_cpf(cpf: str, service: ClienteServicePort = Depends(get_cliente_service)):
    return service.buscar_cliente_por_cpf(cpf)
