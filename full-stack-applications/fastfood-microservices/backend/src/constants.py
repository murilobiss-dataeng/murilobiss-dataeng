"""
Constantes da aplicação.

Este módulo centraliza todas as constantes utilizadas na aplicação,
incluindo mensagens, códigos de status e valores padrão.
"""

# =============================================================================
# MENSAGENS DE RESPOSTA
# =============================================================================

class Messages:
    SUCCESS_CREATED = "Recurso criado com sucesso"
    SUCCESS_UPDATED = "Recurso atualizado com sucesso"
    SUCCESS_DELETED = "Recurso removido com sucesso"
    
    ERROR_NOT_FOUND = "Recurso não encontrado"
    ERROR_INVALID_DATA = "Dados inválidos"
    ERROR_UNAUTHORIZED = "Não autorizado"
    ERROR_FORBIDDEN = "Acesso negado"


# =============================================================================
# CÓDIGOS DE STATUS
# =============================================================================

class StatusCodes:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# =============================================================================
# VALORES PADRÃO
# =============================================================================

class Defaults:
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    MAX_NAME_LENGTH = 100
    MAX_EMAIL_LENGTH = 255 