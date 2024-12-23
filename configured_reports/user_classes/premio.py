from database.entities.other_works import Prize


class Premio:

    nome = "Premio.nome"
    entidade = "Premio.entidade"
    ano = "Premio.ano"

    mapeamento = {
        nome: str(Prize.name),
        entidade: str(Prize.entity),
        ano: str(Prize.year)
    }

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)