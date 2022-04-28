class Capitulo:
    
    titulo = "Capitulo.titulo"
    titulo_livro = "Capitulo.titulo_livro"
    editora = "Capitulo.editora"
    ano = "Capitulo.ano"
    autores = "Capitulo.autores"
    
    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)