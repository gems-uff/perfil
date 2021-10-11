from sqlalchemy import or_, not_, and_
from config import conferences_qualis, conferences_synonyms, conferences_minimum_similarity, journals_qualis, \
    journals_synonyms, journals_minimum_similarity, jcr
from database.paper import JournalPaper, ConferencePaper, Paper
from database.researcher import Researcher
from database.venue import Conference, Journal, QualisLevel
from utils.similarity_manager import detect_similar


def get_qualis_value_from_xlsx(venue_name, similarity_dict, is_conference: bool):
    """Gets the qualis value of a conference or journal from the xlsx file"""
    qualis_dictionary = synonyms_dictionary = minimum_similarity = None
    if is_conference:
        qualis_dictionary = conferences_qualis
        synonyms_dictionary = conferences_synonyms
        minimum_similarity = conferences_minimum_similarity
    else:
        qualis_dictionary = journals_qualis
        synonyms_dictionary = journals_synonyms
        minimum_similarity = journals_minimum_similarity

    # direct match
    if venue_name in qualis_dictionary:
        return qualis_dictionary[venue_name]

    # if direct match fails, try to match using the synonyms file
    for venue_key in synonyms_dictionary:
        if venue_name in synonyms_dictionary[venue_key] and venue_key in qualis_dictionary:
            return qualis_dictionary[venue_key]

    # already matched similar texts
    for venue_key in similarity_dict:
        if len(similarity_dict[venue_key]) > 0 and venue_name in similarity_dict[venue_key] \
                and venue_key in qualis_dictionary:
            return qualis_dictionary[venue_key]

    # lcs
    lcs = detect_similar(venue_name, similarity_dict, minimum_similarity)
    if lcs is not None and lcs in qualis_dictionary: return qualis_dictionary[lcs]

    return None


def get_or_create_conference(session, conference_name, similarity_dict):
    """Gets a conference or populates the Conference table"""
    conference_list = session.query(Conference).filter(Conference.name == conference_name).all()

    if len(conference_list) == 0:
        qualis = get_qualis_value_from_xlsx(conference_name, similarity_dict, True)
        if qualis is not None: qualis = qualis_switch(qualis)
        acronym = None
        try:
            acronym = conference_name[conference_name.index("(") + 1:conference_name.index(")")]
        except:
            pass

        conference = Conference(name=conference_name, qualis=qualis, acronym=acronym)
        session.add(conference)
        session.flush()
        return conference.id

    return conference_list[0].id


def get_or_create_journal(session, journal_details, similarity_dict):
    """Gets a journal or populates the Journal table"""
    journal_issn = journal_details.get("ISSN")[:4] + "-" + journal_details.get("ISSN")[-4:]
    journal_list = session.query(Journal).filter(Journal.issn == journal_issn).all()

    if len(journal_list) == 0:
        journal_name = journal_details.get("TITULO-DO-PERIODICO-OU-REVISTA")
        journal_jcr = jcr[journal_issn] if journal_issn in jcr else 0
        qualis = get_qualis_value_from_xlsx(journal_name, similarity_dict, False)
        if qualis is not None: qualis = qualis_switch(qualis)

        journal = Journal(name=journal_name, issn=journal_issn, jcr=journal_jcr, qualis=qualis)
        session.add(journal)
        session.flush()

        return journal.id

    return journal_list[0].id


def qualis_switch(qualis_value):
    qualis = {
        "A1": QualisLevel.A1,
        "A2": QualisLevel.A2,
        "B1": QualisLevel.B1,
        "B2": QualisLevel.B2,
        "B3": QualisLevel.B3,
        "B4": QualisLevel.B4,
        "B5": QualisLevel.B5,
        "C": QualisLevel.C,
        "NC": QualisLevel.NC
    }

    return qualis[qualis_value.strip()]


def add_journal_papers(session, tree, researcher_id, journals_similarity_dict):
    """Populates the JournalPaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO")
    papers_and_venue_id = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-ARTIGO",
                                     details_attribute="DETALHAMENTO-DO-ARTIGO", title_attribute="TITULO-DO-ARTIGO",
                                     year_attribute="ANO-DO-ARTIGO", session=session,
                                     similarity_dict=journals_similarity_dict)
    researcher = session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

    for paper_venueid in papers_and_venue_id:
        paper = paper_venueid[0]
        venue_id = paper_venueid[1]
        if len(session.query(JournalPaper).filter(JournalPaper.title == paper.title, or_(JournalPaper.doi == paper.doi,
                                                                                         JournalPaper.doi is None)).all()) == 0:
            new_journal_paper = JournalPaper(title=paper.title, doi=paper.doi, year=paper.year,
                                             first_page=paper.first_page,
                                             last_page=paper.last_page, authors=paper.authors, venue=venue_id)
            session.flush()
            new_journal_paper.researchers.append(researcher)


def add_conference_papers(session, tree, researcher_id, conferences_similarity_dict):
    """Populates the ConferencePaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS")
    papers_and_venue_id = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-TRABALHO",
                                     details_attribute="DETALHAMENTO-DO-TRABALHO", title_attribute="TITULO-DO-TRABALHO",
                                     year_attribute="ANO-DO-TRABALHO", session=session,
                                     similarity_dict=conferences_similarity_dict)
    researcher = session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

    for paper_id in papers_and_venue_id:
        paper = paper_id[0]
        venue_id = paper_id[1]
        if len(session.query(ConferencePaper).filter(ConferencePaper.title == paper.title,
                                                     or_(ConferencePaper.doi == paper.doi,
                                                         ConferencePaper.doi is None)).all()) == 0:
            new_conference_paper = ConferencePaper(title=paper.title, doi=paper.doi, year=paper.year,
                                                   first_page=paper.first_page,
                                                   last_page=paper.last_page, authors=paper.authors, venue=venue_id)
            session.flush()
            new_conference_paper.researchers.append(researcher)


def get_papers(element_list, basic_data_attribute, details_attribute, title_attribute, year_attribute, session,
               similarity_dict):
    """Get basic information on papers from xml"""
    papers = []

    for paper in element_list:
        basic_data = paper.findall(basic_data_attribute)[0]
        paper_details = paper.findall(details_attribute)[0]

        title = basic_data.get(title_attribute)
        doi = basic_data.get("DOI") if basic_data.get("DOI") != "" else None

        year = basic_data.get(year_attribute)
        first_page = paper_details.get("PAGINA-INICIAL")
        last_page = paper_details.get("PAGINA-FINAL")
        authors = ""
        venue_id = get_or_add_paper_venue_id(session, details_attribute, paper_details, similarity_dict)

        for author in paper.findall("AUTORES"):
            authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
        authors = authors[:-1]

        papers.append([
            Paper(title=title, doi=doi, year=year, first_page=first_page, last_page=last_page, authors=authors),
            venue_id])

    return papers


def get_or_add_paper_venue_id(session, details_attribute, paper_details, similarity_dict):
    """Auxiliar function to choose which function to call"""
    if details_attribute == "DETALHAMENTO-DO-TRABALHO":
        venue_name = paper_details.get("NOME-DO-EVENTO")
        return get_or_create_conference(session, venue_name, similarity_dict)
    else:
        return get_or_create_journal(session, paper_details, similarity_dict)


def add_coauthor_papers(session):
    """Updates the researcher_journal_paper and researcher_conference_paper from coauthors which didn't have the
    relationship """
    # The code looks like to be duplicated, but the entities/classes/tables are different

    coauthors_and_conference_papers = session.query(Researcher, ConferencePaper).filter(
        ConferencePaper.authors.contains(Researcher.name)).all()
    for relation in coauthors_and_conference_papers:
        researcher = relation[0]
        paper = relation[1]
        if paper not in researcher.conference_papers: researcher.conference_papers.append(paper)

    coauthors_and_journal_papers = session.query(Researcher, JournalPaper).filter(
        JournalPaper.authors.contains(Researcher.name)).all()
    for relation in coauthors_and_journal_papers:
        researcher = relation[0]
        paper = relation[1]
        if paper not in researcher.journal_papers: researcher.journal_papers.append(paper)
