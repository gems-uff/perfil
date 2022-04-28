class Patente:

    nome = "Patente.nome"
    tipo = "Patente.tipo"
    autores = "Patente.autores"
    local = "Patente.local"
    numero = "Patente.numero"
    ano = "Patente.ano"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)