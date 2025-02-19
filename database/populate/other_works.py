import uuid
from sqlalchemy import and_, func
from utils.log import log_possible_lattes_duplication, log_unify
from database.entities.researcher import Researcher
from database.entities.other_works import ConferenceOrganization, EditorialBoard, EditorialBoardType, Prize, \
    ResearcherPatent, Patent, PatentType
from config import unify_patent, areas


def add_researcher_conference_management(session, tree, researcher):
    '''Adds all conferences managed by the researcher from a lattes .xml file'''
    conferences_managed = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-TECNICA/DEMAIS-TIPOS-DE-PRODUCAO-TECNICA/ORGANIZACAO-DE-EVENTO")
    researcher_name = researcher.name

    for conference in conferences_managed:
        basic_data = conference.findall("DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO")[0]

        title = basic_data.get("TITULO")
        year = basic_data.get("ANO")
        committee = ""

        for member in conference.findall("AUTORES"):
            committee += member.get("NOME-COMPLETO-DO-AUTOR") + ";"
        committee = committee[:-1]

        # Lattes duplication
        lattes_duplication = session.query(ConferenceOrganization).filter(
            and_(ConferenceOrganization.researcher_id == researcher.id,
                 func.lower(ConferenceOrganization.title) == func.lower(title), ConferenceOrganization.year == year)).all()

        if len(lattes_duplication) > 0:
            log_possible_lattes_duplication("researcher_conference_management", researcher_name, researcher.id, title, year)

        session.add(ConferenceOrganization(researcher_id=researcher.id, title=title, year=year, committee=committee))


def add_researcher_editorial_board(session, tree, researcher):
    '''Adds all the jobs of a researcher while working in journals from the lattes .xml file'''
    jobs = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL")
    researcher_name = researcher.name

    for job in jobs:
        contracts = job.findall("VINCULOS")
        if contracts:
            contract = contracts[0]
            other_link = contract.get("OUTRO-VINCULO-INFORMADO")

            if ("Membro de corpo editorial" in other_link) or ("Revisor de peri" in other_link):
                start_year = contract.get("ANO-INICIO")
                end_year = contract.get("ANO-FIM")
                type = editorial_board_type_switch(other_link)
                journal_name = job.get("NOME-INSTITUICAO")

                # Lattes duplication
                lattes_duplication = session.query(EditorialBoard).filter(
                    and_(EditorialBoard.researcher_id == researcher.id,
                        func.lower(EditorialBoard.journal_name) == func.lower(journal_name), EditorialBoard.type == type,
                        EditorialBoard.start_year == start_year)).all()

                if len(lattes_duplication) > 0:
                    log_possible_lattes_duplication("reseacher_editorial_board", researcher_name, researcher.id, journal_name, type, start_year)

                session.add(EditorialBoard(researcher_id=researcher.id, journal_name=journal_name, type=type,
                                        start_year=start_year, end_year=end_year))


def editorial_board_type_switch(other_link):
    '''Auxiliar function to choose the correct type of editorial board job'''
    if "Membro" in other_link:
        return EditorialBoardType.EDITORIAL_BOARD
    elif "Revisor" in other_link:
        return EditorialBoardType.REVIEWER


def add_researcher_patents_software(session, tree, researcher):
    '''Adds all the software pantents or ordinary patents from a lattes .xml file'''
    programs = tree.xpath("/CURRICULO-VITAE/PRODUCAO-TECNICA/SOFTWARE")
    researcher_name = researcher.name

    for program in programs:
        program_patent = get_or_add_patent(session, program, True, researcher.id, researcher_name)

        check_lattes_duplication_patent(program_patent, researcher.id, researcher_name, session)

        if program_patent is not None:
            if len(session.query(ResearcherPatent).filter(ResearcherPatent.researcher_id == researcher.id,
                                                          ResearcherPatent.patent_id == program_patent.id).all()) == 0:
                session.add(ResearcherPatent(patent_id=program_patent.id, researcher_id=researcher.id))

    patents = tree.xpath("/CURRICULO-VITAE/PRODUCAO-TECNICA/PATENTE")

    for patent in patents:
        patent_in_db = get_or_add_patent(session, patent, False, researcher.id, researcher_name)

        check_lattes_duplication_patent(patent_in_db, researcher.id, researcher_name, session)

        if patent_in_db is not None:
            if len(session.query(ResearcherPatent).filter(ResearcherPatent.researcher_id == researcher.id, ResearcherPatent.patent_id == patent_in_db.id).all()) == 0:
                session.add(ResearcherPatent(patent_id=patent_in_db.id, researcher_id=researcher.id))


def get_or_add_patent(session, patent, software_patent: bool, researcher_id, researcher_name):
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

    # Normalize
    if unify_patent and (len(patent_list) > 0):
        log_unify(patent_list[0].number, researcher_id, researcher_name)
        return patent_list[0]

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

    return new_patent


def check_lattes_duplication_patent(patent, researcher_id, researcher_name, session):
    this_researcher_patent_relationship = session.query(ResearcherPatent.patent_id).filter(ResearcherPatent.researcher_id == researcher_id)
    this_researcher_patents_in_db = session.query(Patent).filter(Patent.number == patent.number, Patent.id.in_(this_researcher_patent_relationship)).all()

    for patent_in_db in this_researcher_patents_in_db:
        log_possible_lattes_duplication("researcher_patent", researcher_name, researcher_id, patent_in_db.id,
                                            patent_in_db.title, patent_in_db.year, patent_in_db.number)
        

def add_researcher_prizes(session, tree, researcher):
    '''Adds all prizes from a lattes .xml file'''
    lattes_prizes = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/PREMIOS-TITULOS/PREMIO-TITULO")

    for lattes_prize in lattes_prizes:
        name = lattes_prize.get("NOME-DO-PREMIO-OU-TITULO")
        entity = lattes_prize.get("NOME-DA-ENTIDADE-PROMOTORA")
        year = lattes_prize.get("ANO-DA-PREMIACAO")
                
        session.add(Prize(researcher=researcher, name=name, entity=entity, year=year))


def check_lattes_duplication_patent(patent, researcher_id, researcher_name, session):
    this_researcher_patent_relationship = session.query(ResearcherPatent.patent_id).filter(ResearcherPatent.researcher_id == researcher_id)
    this_researcher_patents_in_db = session.query(Patent).filter(Patent.number == patent.number, Patent.id.in_(this_researcher_patent_relationship)).all()

    for patent_in_db in this_researcher_patents_in_db:
        log_possible_lattes_duplication("researcher_patent", researcher_name, researcher_id, patent_in_db.id,
                                            patent_in_db.title, patent_in_db.year, patent_in_db.number)