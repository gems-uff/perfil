import uuid
from sqlalchemy import and_
from utils.log import log_primary_key_error
from database.other_works import ResearcherConferenceManagement, ResearcherEditorialBoard, EditorialBoardType, \
    ResearcherPatent, Patent, PatentType


def add_researcher_conference_management(session, tree, researcher_id):
    '''Adds all conferences managed by the researcher from a lattes .xml file'''
    conferences_managed = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-TECNICA/DEMAIS-TIPOS-DE-PRODUCAO-TECNICA/ORGANIZACAO-DE-EVENTO")

    for conference in conferences_managed:
        basic_data = conference.findall("DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO")[0]

        title = basic_data.get("TITULO")
        year = basic_data.get("ANO")
        committee = ""

        for member in conference.findall("AUTORES"):
            committee += member.get("NOME-COMPLETO-DO-AUTOR") + ";"
        committee = committee[:-1]

        lattes_duplication = session.query(ResearcherConferenceManagement).filter(
            and_(ResearcherConferenceManagement.researcher_id==researcher_id,
                 ResearcherConferenceManagement.title==title, ResearcherConferenceManagement.year == year)).all()

        if len(lattes_duplication) > 0: log_primary_key_error("researcher_conference_management", researcher_id,
                                                               title, year)
        else: session.add(ResearcherConferenceManagement(researcher_id=researcher_id, title=title, year=year,
                                                         committee=committee))


def add_researcher_editorial_board(session, tree, researcher_id):
    '''Adds all the jobs of a researcher while working in journals from the lattes .xml file'''
    jobs = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL")

    for job in jobs:
        info = job.findall("VINCULOS")[0]
        other_link = info.get("OUTRO-VINCULO-INFORMADO")

        if ("Membro de corpo editorial" in other_link) or ("Revisor de peri" in other_link):
            begin_year = info.get("ANO-INICIO")
            end_year = info.get("ANO-FIM")
            type = editorial_board_type_switch(other_link)
            journal_name = job.get("NOME-INSTITUICAO")

            lattes_duplication = session.query(ResearcherEditorialBoard).filter(
                and_(ResearcherEditorialBoard.researcher_id==researcher_id,
                     ResearcherEditorialBoard.journal_name==journal_name, ResearcherEditorialBoard.type==type,
                     ResearcherEditorialBoard.begin_year==begin_year)).all()

            if len(lattes_duplication) > 0: log_primary_key_error("reseacher_editorial_board", researcher_id,
                                                                  journal_name, type, begin_year)
            else: session.add(ResearcherEditorialBoard(researcher_id=researcher_id, journal_name=journal_name, type=type,
                                                 begin_year=begin_year, end_year=end_year))


def editorial_board_type_switch(other_link):
    '''Auxiliar function to choose the correct type of editorial board job'''
    if "Membro" in other_link:
        return EditorialBoardType.EDITORIAL_BOARD
    elif "Revisor" in other_link:
        return EditorialBoardType.REVISER


def add_researcher_patents_software(session, tree, researcher_id):
    '''Adds all the software pantents or ordinary patents from a lattes .xml file'''
    programs = tree.xpath("/CURRICULO-VITAE/PRODUCAO-TECNICA/SOFTWARE")

    for program in programs:
        program_patent_id = get_or_add_patent(session, program, True)

        if program_patent_id is not None: session.add(ResearcherPatent(patent_id=program_patent_id, researcher_id=researcher_id))

    patents = tree.xpath("/CURRICULO-VITAE/PRODUCAO-TECNICA/PATENTE")

    for patent in patents:
        patent_id = get_or_add_patent(session, patent, False)

        if patent_id is not None: session.add(ResearcherPatent(patent_id=patent_id, researcher_id=researcher_id))


def get_or_add_patent(session, patent, software_patent: bool):
    '''Gets a patent already on the database or adds it'''
    basic_data = None
    patent_details = None

    if software_patent:
        basic_data = patent.findall("DADOS-BASICOS-DO-SOFTWARE")
        patent_details = patent.findall("DETALHAMENTO-DO-SOFTWARE/REGISTRO-OU-PATENTE")
    else:
        basic_data = patent.findall("DADOS-BASICOS-DA-PATENTE")
        patent_details = patent.findall("DETALHAMENTO-DA-PATENTE/REGISTRO-OU-PATENTE")

    if len(basic_data) == 0: return None
    basic_data = basic_data[0]
    patent_details = patent_details[0] if len(patent_details) > 0 else None

    number = str(uuid.uuid4())
    title = local_of_registry = None
    if patent_details is not None:
        number = patent_details.get("CODIGO-DO-REGISTRO-OU-PATENTE")
        title = patent_details.get("TITULO-PATENTE")
        local_of_registry = patent_details.get("INSTITUICAO-DEPOSITO-REGISTRO")

    patent_list = session.query(Patent).filter(Patent.number == number).all()

    if len(patent_list) > 0:
        return patent_list[0].id

    year = None
    type = None
    if software_patent:
        year = basic_data.get("ANO")
        type = PatentType.SOFTWARE
    else:
        year = basic_data.get("ANO-DESENVOLVIMENTO")
        type = PatentType.PATENT

    authors = ""
    for author in patent.findall("AUTORES"):
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]
    new_patent = Patent(type=type, title=title, number=number, local_of_registry=local_of_registry,
                        year=year, authors=authors)
    session.add(new_patent)
    session.flush()

    return new_patent.id