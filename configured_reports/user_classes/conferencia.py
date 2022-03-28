class Conferencia:

    artigo = "Conferencia.artigo"
    tipo_artigo = "Conferencia.tipo_artigo"
    ano = "Conferencia.ano"
    doi = "Conferencia.doi"
    quantidade_paginas = "Conferencia.quantidade_paginas"
    autores = "Conferencia.autores"
    nome = "Conferencia.nome"
    qualis = "Conferencia.qualis"
    qualis_pontos = "Conferencia.qualis_pontos"
    forum_oficial = "Conferencia.forum_oficial"
    acronimo = "Conferencia.acronimo"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)