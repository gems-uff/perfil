class Pesquisador:

    nome = "Pesquisador.nome"
    ultima_atualizacao_lattes = "Pesquisador.ultima_atualizacao_lattes"
    doutorado_universidade = "Pesquisador.doutorado_universidade"
    doutorado_ano = "Pesquisador.doutorado_ano"
    id_google_scholar = "Pesquisador.id_google_scholar"
    id_lattes = "Pesquisador.id_lattes"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)