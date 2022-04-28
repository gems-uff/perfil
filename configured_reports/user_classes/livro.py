class Livro:

    titulo = "Livro.titulo"
    editora = "Livro.editora"
    ano = "Livro.ano"
    autores = "Livro.autores"

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)