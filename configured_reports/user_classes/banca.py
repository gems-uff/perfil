class Banca:

    tipo = "Banca.tipo"
    ano = "Banca.ano"
    universidade = "Banca.universidade"
    aluno_ou_cargo = "Banca.aluno_ou_cargo"
    titulo = "Banca.titulo"
    membros = "Banca.membros"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)