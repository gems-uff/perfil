from database.entities.researcher import Education


class Formacao:

    tipo = "Formacao.tipo"
    curso = "Formacao.curso"
    area = "Formacao.area"
    instituicao = "Formacao.instituicao"
    inicio = "Formacao.inicio"
    fim = "Formacao.fim"

    mapeamento = {
        tipo: str(Education.type),
        curso: str(Education.course),
        area: str(Education.area),
        instituicao: str(Education.institution),
        inicio: str(Education.start_date),
        fim: str(Education.end_date)
    }

    def __init__(self):
        pass

    def __repr__(self):
        return str(self.__dict__)