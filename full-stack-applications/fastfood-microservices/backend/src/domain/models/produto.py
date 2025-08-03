class Produto:
    def __init__(self, id, nome, categoria, preco, estoque=100):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.estoque_reservado = 0

    def esta_disponivel(self, quantidade: int) -> bool:
        """Verifica se há estoque disponível para a quantidade solicitada"""
        return (self.estoque - self.estoque_reservado) >= quantidade

    def reservar_estoque(self, quantidade: int) -> bool:
        """Reserva estoque para um pedido"""
        if self.esta_disponivel(quantidade):
            self.estoque_reservado += quantidade
            return True
        return False

    def liberar_estoque(self, quantidade: int) -> None:
        """Libera estoque reservado"""
        if self.estoque_reservado >= quantidade:
            self.estoque_reservado -= quantidade
        else:
            self.estoque_reservado = 0

    def confirmar_estoque(self, quantidade: int) -> None:
        """Confirma a reserva de estoque, reduzindo o estoque real"""
        if self.estoque_reservado >= quantidade:
            self.estoque -= quantidade
            self.estoque_reservado -= quantidade
