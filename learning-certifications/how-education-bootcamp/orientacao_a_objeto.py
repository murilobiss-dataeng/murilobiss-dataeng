import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos."

murilo = Pessoa(nome='Murilo', sobrenome='Biss', data_de_nascimento=datetime.date(1987, 12, 6))

print(murilo)
print(murilo.nome)
print(murilo.sobrenome)
print(murilo.data_de_nascimento)
print(murilo.idade)