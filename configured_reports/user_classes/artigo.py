class Artigo:

    artigo = "Artigo.artigo"
    tipo_artigo = "Artigo.tipo_artigo"
    ano = "Artigo.ano"
    doi = "Artigo.doi"
    quantidade_paginas = "Artigo.quantidade_paginas"
    autores = "Artigo.autores"
    nome = "Artigo.nome"
    qualis = "Artigo.qualis"
    qualis_pontos = "Artigo.qualis_pontos"
    forum_oficial = "Artigo.forum_oficial"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)