"""
Utilitários da aplicação.

Este módulo contém funções auxiliares e utilitários utilizados
em diferentes partes da aplicação.
"""

import re
from typing import List
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    Valida se um email está no formato correto.
    
    Args:
        email: Email a ser validado
        
    Returns:
        True se o email é válido, False caso contrário
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Valida se um telefone está no formato correto.
    
    Args:
        phone: Telefone a ser validado
        
    Returns:
        True se o telefone é válido, False caso contrário
    """
    # Remove caracteres não numéricos
    phone_clean = re.sub(r'[^\d]', '', phone)
    # Verifica se tem entre 10 e 11 dígitos
    return 10 <= len(phone_clean) <= 11


def format_currency(value: float) -> str:
    """
    Formata um valor monetário para exibição.
    
    Args:
        value: Valor a ser formatado
        
    Returns:
        String formatada com o valor monetário
    """
    return f"R$ {value:.2f}".replace('.', ',')


def sanitize_string(text: str) -> str:
    """
    Remove caracteres especiais e normaliza uma string.
    
    Args:
        text: Texto a ser sanitizado
        
    Returns:
        String sanitizada
    """
    if not text:
        return ""
    
    # Remove caracteres especiais e normaliza espaços
    sanitized = re.sub(r'[^\w\s-]', '', text)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    return sanitized


def get_current_timestamp() -> datetime:
    """
    Retorna o timestamp atual em UTC.
    
    Returns:
        Timestamp atual
    """
    return datetime.now()


def generate_order_number() -> str:
    """
    Gera um número de pedido único.
    
    Returns:
        String com o número do pedido
    """
    timestamp = get_current_timestamp()
    return f"PED{timestamp.strftime('%Y%m%d%H%M%S')}" 