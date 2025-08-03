import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date) -> None:
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos."

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: list[str]):
            self.experiencias = experiencias
            self.pessoa = pessoa
    
    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)
    
    def __str__(self):
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos, já" \
            f" trabalhou em {self.quantidade_de_experiencias} empresas e atualmente" \
            f" trabalha na empresa {self.empresa_atual}."

murilo = Pessoa(nome='Murilo', sobrenome='Biss', data_de_nascimento=datetime.date(1987, 12, 6))

curriculo_murilo = Curriculo(
    pessoa=murilo, 
    experiencias=['HSBC','Bradesco','Renault','Bari'])

class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruido: {ruido}")

class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos."

    def fala(self, frase):
        return self.emite_ruido(frase)

class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raça: str):
        super().__init__(nome, data_de_nascimento)
        self.raça = raça

    def __str__(self) -> str:
        return f"{self.nome} é da raça {self.raça} tem {self.idade} anos."

    def late(self):
        return self.emite_ruido("Au! Au!")

murilo2 = PessoaHeranca(nome='Murilo',data_de_nascimento=datetime.date(1987,12,6))

bela = Cachorro(nome='Bela', data_de_nascimento=datetime.date(2018,5,5), raça='Vira-lata')
