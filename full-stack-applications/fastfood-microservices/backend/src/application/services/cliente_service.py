from uuid import uuid4

from src.adapters.input.dto.cliente_dto import ClienteCreate, ClienteResponse
from src.domain.models.cliente import Cliente
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort
from src.ports.services.cliente_service_port import ClienteServicePort


class ClienteService(ClienteServicePort):
    def __init__(self, cliente_repository: ClienteRepositoryPort):
        self.cliente_repository = cliente_repository

    def criar_ou_obter_cliente(self, cliente_create: ClienteCreate) -> ClienteResponse:
        if cliente_create.cpf:
            cliente = self.cliente_repository.buscar_por_cpf(cliente_create.cpf)
            if cliente:
                return ClienteResponse(**cliente.__dict__)

        if cliente_create.email:
            cliente = self.cliente_repository.buscar_por_email(cliente_create.email)
            if cliente:
                return ClienteResponse(**cliente.__dict__)

        # Cria cliente novo (ou anônimo)
        cliente = Cliente(
            id=uuid4(),
            nome=cliente_create.nome,
            cpf=cliente_create.cpf,
            email=cliente_create.email,
        )
        self.cliente_repository.salvar(cliente)
        return ClienteResponse(**cliente.__dict__)

    def buscar_cliente_por_cpf(self, cpf: str) -> ClienteResponse | None:
        cliente = self.cliente_repository.buscar_por_cpf(cpf)
        if cliente:
            return ClienteResponse(**cliente.__dict__)
        return None

    def listar_clientes(self) -> list[ClienteResponse]:
        clientes = self.cliente_repository.listar()
        return [ClienteResponse(**c.__dict__) for c in clientes]
