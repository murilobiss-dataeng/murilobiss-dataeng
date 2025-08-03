import re
from uuid import UUID, uuid4
from datetime import UTC, datetime
from typing import Optional


class Cliente:
    def __init__(
        self,
        id: UUID,
        nome: str,
        email: Optional[str] = None,
        cpf: Optional[str] = None,
        data_criacao: datetime | None = None,
        ativo: bool = True,
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_criacao = data_criacao or datetime.now(UTC)
        self.ativo = ativo
        
        # Validações de domínio
        self._validar_cliente()

    @classmethod
    def criar(
        cls, 
        nome: str, 
        email: Optional[str] = None, 
        cpf: Optional[str] = None
    ) -> "Cliente":
        """Factory method para criar um novo cliente com validações"""
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório")
        
        if len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome.strip()) > 100:
            raise ValueError("Nome não pode ter mais de 100 caracteres")
        
        if email and not cls._validar_email(email):
            raise ValueError("Email inválido")
        
        if cpf and not cls._validar_cpf(cpf):
            raise ValueError("CPF inválido")
        
        return cls(
            id=uuid4(),
            nome=nome.strip(),
            email=email.strip() if email else None,
            cpf=cls._formatar_cpf(cpf) if cpf else None,
            data_criacao=datetime.now(UTC),
            ativo=True,
        )

    @classmethod
    def criar_anonimo(cls) -> "Cliente":
        """Cria um cliente anônimo para pedidos sem identificação"""
        return cls(
            id=uuid4(),
            nome="Cliente Anônimo",
            email=None,
            cpf=None,
            data_criacao=datetime.now(UTC),
            ativo=True,
        )

    def atualizar_dados(self, nome: Optional[str] = None, email: Optional[str] = None) -> None:
        """Atualiza os dados do cliente com validações"""
        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome não pode ser vazio")
            if len(nome.strip()) < 2:
                raise ValueError("Nome deve ter pelo menos 2 caracteres")
            if len(nome.strip()) > 100:
                raise ValueError("Nome não pode ter mais de 100 caracteres")
            self.nome = nome.strip()
        
        if email is not None:
            if email and not self._validar_email(email):
                raise ValueError("Email inválido")
            self.email = email.strip() if email else None

    def desativar(self) -> None:
        """Desativa o cliente"""
        self.ativo = False

    def ativar(self) -> None:
        """Ativa o cliente"""
        self.ativo = True

    def eh_anonimo(self) -> bool:
        """Verifica se o cliente é anônimo"""
        return self.nome == "Cliente Anônimo" and not self.email and not self.cpf

    def pode_fazer_pedido(self) -> bool:
        """Verifica se o cliente pode fazer pedidos"""
        return self.ativo

    def obter_identificacao(self) -> str:
        """Retorna a identificação principal do cliente"""
        if self.cpf:
            return self.cpf
        elif self.email:
            return self.email
        else:
            return str(self.id)

    @staticmethod
    def _validar_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida CPF usando algoritmo oficial"""
        # Remove caracteres não numéricos
        cpf_numeros = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf_numeros) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if len(set(cpf_numeros)) == 1:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(cpf_parcial: str) -> int:
            soma = sum(int(cpf_parcial[i]) * (10 - i) for i in range(len(cpf_parcial)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Primeiro dígito verificador
        if int(cpf_numeros[9]) != calcular_digito(cpf_numeros[:9]):
            return False
        
        # Segundo dígito verificador
        if int(cpf_numeros[10]) != calcular_digito(cpf_numeros[:10]):
            return False
        
        return True

    @staticmethod
    def _formatar_cpf(cpf: str) -> str:
        """Formata CPF no padrão XXX.XXX.XXX-XX"""
        cpf_numeros = re.sub(r'[^0-9]', '', cpf)
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

    def _validar_cliente(self) -> None:
        """Validações internas do cliente"""
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome é obrigatório")
        
        if self.email and not self._validar_email(self.email):
            raise ValueError("Email inválido")
        
        if self.cpf and not self._validar_cpf(self.cpf):
            raise ValueError("CPF inválido")

    def __str__(self) -> str:
        if self.eh_anonimo():
            return "Cliente Anônimo"
        return f"{self.nome} ({self.obter_identificacao()})"

    def __repr__(self) -> str:
        return f"Cliente(id={self.id}, nome='{self.nome}', ativo={self.ativo})"
