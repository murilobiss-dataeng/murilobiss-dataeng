"""
Exceções customizadas da aplicação.

Este módulo define exceções específicas da aplicação para melhor
tratamento e identificação de erros.
"""

from fastapi import HTTPException
from typing import Any


class BaseAppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ResourceNotFoundException(BaseAppException):
    def __init__(self, resource: str, resource_id: Any):
        detail = f"{resource} com ID {resource_id} não encontrado"
        super().__init__(status_code=404, detail=detail)


class ValidationException(BaseAppException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class BusinessRuleException(BaseAppException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class AuthenticationException(BaseAppException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=401, detail=detail) 