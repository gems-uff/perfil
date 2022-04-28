class Periodico:

    artigo = "Periodico.artigo"
    tipo_artigo = "Periodico.tipo_artigo"
    ano = "Periodico.ano"
    doi = "Periodico.doi"
    artigo_aceito = "Periodico.artigo_aceito"
    quantidade_paginas = "Periodico.quantidade_paginas"
    autores = "Periodico.autores"
    nome = "Periodico.nome"
    forum_oficial = "Periodico.forum_oficial"
    qualis = "Periodico.qualis"
    qualis_pontos = "Periodico.qualis_pontos"
    issn = "Periodico.issn"
    jcr = "Periodico.jcr"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)