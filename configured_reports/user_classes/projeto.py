class Projeto:

    nome = "Projeto.nome"
    responsavel = "Projeto.responsavel"
    coordenador = "Projeto.coordenador"
    equipe = "Projeto.equipe"
    inicio = "Projeto.inicio"
    fim = "Projeto.fim"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)