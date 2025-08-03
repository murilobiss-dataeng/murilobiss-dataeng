from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    cpf: str | None = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: UUID
