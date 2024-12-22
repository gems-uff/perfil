import math
from sqlalchemy import or_, not_, and_, func
from config import conferences_qualis, conferences_synonyms, conferences_minimum_similarity, \
    conferences_papers_title_minimum_similarity, journals_qualis, issn_journals, journals_synonyms, journals_minimum_similarity, \
    journals_papers_title_minimum_similarity, jcr, unify_conference_paper, unify_journal_paper, QualisLevel, qualis_switch
from database.entities.paper import JournalPaper, ConferencePaper, Paper, PaperNature
from database.entities.researcher import Researcher
from database.entities.venue import Conference, Journal
from utils.similarity_manager import detect_similar, get_similarity
from utils.log import log_unify, log_possible_lattes_duplication

def get_qualis_value_from_xlsx(venue_issn, venue_name, similarity_dict, is_conference: bool):
    """Gets the qualis value of a conference or journal from the xlsx qualis file"""
    qualis_dictionary = synonyms_dictionary = minimum_similarity = None
    if is_conference:
        qualis_dictionary = conferences_qualis
        synonyms_dictionary = conferences_synonyms
        minimum_similarity = conferences_minimum_similarity
    else:
        qualis_dictionary = journals_qualis
        synonyms_dictionary = journals_synonyms
        minimum_similarity = journals_minimum_similarity

    # ISSN match (just for journals)
    if venue_issn in issn_journals: return(qualis_dictionary[issn_journals[venue_issn]], issn_journals[venue_issn])

    # If ISSN match fails, try direct name match
    if venue_name in qualis_dictionary: return (qualis_dictionary[venue_name], venue_name)

    # if direct name match fails, try to match using the synonyms file
    if (venue_name in synonyms_dictionary) and (synonyms_dictionary[venue_name] in qualis_dictionary): return (qualis_dictionary[synonyms_dictionary[venue_name]], synonyms_dictionary[venue_name])

    # if synonyms match fails, try already matched similar texts
    if (venue_name in similarity_dict) and (similarity_dict[venue_name] in qualis_dictionary): return (qualis_dictionary[similarity_dict[venue_name]], similarity_dict[venue_name])

    # lcs
    lcs = detect_similar(venue_name, qualis_dictionary, minimum_similarity, similarity_dict)
    if lcs is not None and lcs in qualis_dictionary: return (qualis_dictionary[lcs], lcs)

    return 'NC', ''


def get_or_create_conference(session, conference_name, similarity_dict):
    """Gets a conference or populates the Conference table"""
    conference_list = session.query(Conference).filter(Conference.name == conference_name).all()

    if len(conference_list) == 0:
        qualis_and_forum = get_qualis_value_from_xlsx(None, conference_name, similarity_dict, True)    
        qualis = qualis_switch[qualis_and_forum[0].strip()]
        forum_oficial = qualis_and_forum[1]
        acronym = None
        try:
                acronym = forum_oficial[forum_oficial.index("(") + 1:forum_oficial.index(")")]                            
        except:
            try:
                acronym = conference_name[conference_name.index("(") + 1:conference_name.index(")")]
            except:
                pass              

        conference = Conference(name=conference_name, qualis=qualis, acronym=acronym, official_forum=forum_oficial)
        session.add(conference)
        session.flush()
        return conference

    return conference_list[0]


def get_or_create_journal(session, journal_details, similarity_dict):
    """Gets a journal or populates the Journal table"""
    journal_issn = journal_details.get("ISSN")[:4] + "-" + journal_details.get("ISSN")[-4:]
    journal_list = session.query(Journal).filter(Journal.issn == journal_issn).all()

    if len(journal_list) == 0:
        journal_name = journal_details.get("TITULO-DO-PERIODICO-OU-REVISTA").upper()
        journal_jcr = jcr[journal_issn] if journal_issn in jcr and not math.isnan(jcr[journal_issn]) else 0

        qualis_and_forum = get_qualis_value_from_xlsx(journal_issn, journal_name, similarity_dict, False)
        qualis = None
        forum_oficial = None
        if qualis_and_forum is not None:
            qualis = qualis_switch[qualis_and_forum[0].strip()]
            forum_oficial = qualis_and_forum[1]

        journal = Journal(name=journal_name, issn=journal_issn, jcr=journal_jcr, qualis=qualis, official_forum=forum_oficial)
        session.add(journal)
        session.flush()

        return journal

    return journal_list[0]


def add_journal_papers(session, tree, researcher, journals_similarity_dict):
    """Adds both published journal papers and accepted ones"""
    add_journal_papers_published_and_accepted(session, tree, researcher, journals_similarity_dict, True)
    add_journal_papers_published_and_accepted(session, tree, researcher, journals_similarity_dict, False)


def add_journal_papers_published_and_accepted(session, tree, researcher, journals_similarity_dict, published):
    """Populates the JournalPaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO") \
        if published else tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-ACEITOS-PARA-PUBLICACAO/ARTIGO-ACEITO-PARA-PUBLICACAO")

    papers_and_venues = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-ARTIGO",
                                     details_attribute="DETALHAMENTO-DO-ARTIGO", title_attribute="TITULO-DO-ARTIGO",
                                     year_attribute="ANO-DO-ARTIGO", session=session,
                                     similarity_dict=journals_similarity_dict)

    for paper_venue in papers_and_venues:
        paper = paper_venue[0]
        venue = paper_venue[1]

        # Lattes duplication
        for this_researcher_paper_in_db in researcher.journal_papers:
            if (this_researcher_paper_in_db.doi == paper.doi and paper.doi is not None and paper.doi != "") \
                    or (this_researcher_paper_in_db.title.lower() == paper.title.lower() and this_researcher_paper_in_db.nature == paper.nature):
                log_possible_lattes_duplication("researcher_journal_paper", researcher.name, researcher.id, this_researcher_paper_in_db.id,
                                                this_researcher_paper_in_db.title, this_researcher_paper_in_db.nature, this_researcher_paper_in_db.doi)
                break

        # Normalize
        journal_papers_in_db = session.query(JournalPaper).filter(
            and_(func.lower(JournalPaper.title) == func.lower(paper.title), JournalPaper.nature == paper.nature),
            or_(JournalPaper.doi == paper.doi, JournalPaper.doi is None, paper.doi is None)).all()

        if unify_journal_paper and (len(journal_papers_in_db) > 0):
            # for each paper paper found in the db, adds the researcher_journal_paper relationship
            for journal_paper in journal_papers_in_db:
                if researcher.name not in journal_paper.authors: journal_paper.authors += ";" + researcher.name
                journal_paper.researchers.append(researcher)
                log_unify(journal_paper.title, researcher.id, researcher.name)
        else:
            accepted = not published
            new_journal_paper = JournalPaper(title=paper.title, doi=paper.doi, year=paper.year, nature=paper.nature,
                                             first_page=paper.first_page, last_page=paper.last_page,
                                             authors=paper.authors, venue=venue.id, accepted=accepted)
            new_journal_paper.researchers.append(researcher)


def add_conference_papers(session, tree, researcher, conferences_similarity_dict):
    """Populates the ConferencePaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS")
    papers_and_venues = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-TRABALHO",
                                     details_attribute="DETALHAMENTO-DO-TRABALHO", title_attribute="TITULO-DO-TRABALHO",
                                     year_attribute="ANO-DO-TRABALHO", session=session,
                                     similarity_dict=conferences_similarity_dict)
    for paper_venue in papers_and_venues:
        paper = paper_venue[0]
        venue = paper_venue[1]

        # Lattes duplication
        for this_researcher_paper_in_db in researcher.conference_papers:
            if (this_researcher_paper_in_db.doi == paper.doi and paper.doi is not None and paper.doi != "") \
                    or (this_researcher_paper_in_db.title.lower() == paper.title.lower() and this_researcher_paper_in_db.nature == paper.nature):
                log_possible_lattes_duplication("researcher_conference_paper", researcher.name, researcher.id, this_researcher_paper_in_db.id,
                                                this_researcher_paper_in_db.title, this_researcher_paper_in_db.nature, this_researcher_paper_in_db.doi)
                break

        # Normalize
        conference_papers_in_db = session.query(ConferencePaper).filter(
            and_(func.lower(ConferencePaper.title) == func.lower(paper.title), ConferencePaper.nature == paper.nature),
            or_(ConferencePaper.doi == paper.doi, ConferencePaper.doi is None, paper.doi is None)).all()

        if unify_conference_paper and (len(conference_papers_in_db) > 0):
            # for each paper paper found in the db, adds the researcher_conference_paper relationship
            for conference_paper in conference_papers_in_db:
                if researcher.name not in conference_paper.authors: conference_paper.authors += ";" + researcher.name
                conference_paper.researchers.append(researcher)
                log_unify(conference_paper.title, researcher.id, researcher.name)
        else:
            new_conference_paper = ConferencePaper(title=paper.title, doi=paper.doi, nature=paper.nature,
                                                   year=paper.year, first_page=paper.first_page,
                                                   last_page=paper.last_page, authors=paper.authors, venue=venue.id)
            new_conference_paper.researchers.append(researcher)


def get_papers(element_list, basic_data_attribute, details_attribute, title_attribute, year_attribute, session,
               similarity_dict):
    """Get basic information of the papers from the xml"""
    papers = []

    for paper in element_list:
        basic_data = paper.findall(basic_data_attribute)[0]
        paper_details = paper.findall(details_attribute)[0]

        title = basic_data.get(title_attribute)
        doi = basic_data.get("DOI") if basic_data.get("DOI") != "" else None
        nature = nature_switch(basic_data.get("NATUREZA"))

        year = int(basic_data.get(year_attribute))
        first_page = paper_details.get("PAGINA-INICIAL")
        try: first_page = int(first_page)
        except: pass
        last_page = paper_details.get("PAGINA-FINAL")
        try: last_page = int(last_page)
        except: pass
        authors = ""
        venue = get_or_add_paper_venue(session, details_attribute, paper_details, similarity_dict)

        for author in paper.findall("AUTORES"):
            authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
        authors = authors[:-1]

        papers.append([
            Paper(title=title, doi=doi, nature=nature, year=year, first_page=first_page, last_page=last_page,
                  authors=authors), venue])

    return papers


def nature_switch(basic_data_nature):
    nature = {
        "COMPLETO": PaperNature.COMPLETE,
        "RESUMO": PaperNature.ABSTRACT,
        "RESUMO_EXPANDIDO": PaperNature.EXPANDED_ABSTRACT
    }

    if basic_data_nature in nature: return nature[basic_data_nature]
    return None


def get_or_add_paper_venue(session, details_attribute, paper_details, similarity_dict):
    """Auxiliar function to choose which function to call"""
    if details_attribute == "DETALHAMENTO-DO-TRABALHO":
        venue_name = paper_details.get("NOME-DO-EVENTO").upper()
        return get_or_create_conference(session, venue_name, similarity_dict)
    else:
        return get_or_create_journal(session, paper_details, similarity_dict)


def add_coauthor_papers(session):
    """Updates the researcher_journal_paper and researcher_conference_paper for coauthors which didn't have the
    relationship """
    # The code looks like to be duplicated, but the entities/classes/tables are different
    if unify_conference_paper:

        coauthors_and_conference_papers = session.query(Researcher, ConferencePaper).filter(
            ConferencePaper.authors.contains(Researcher.name)).all()
        for relation in coauthors_and_conference_papers:
            researcher = relation[0]
            paper = relation[1]
            add_papers_different_titles(paper, researcher.conference_papers, conferences_papers_title_minimum_similarity, researcher)

    if unify_journal_paper:

        coauthors_and_journal_papers = session.query(Researcher, JournalPaper).filter(
            JournalPaper.authors.contains(Researcher.name)).all()
        for relation in coauthors_and_journal_papers:
            researcher = relation[0]
            paper = relation[1]
            add_papers_different_titles(paper, researcher.journal_papers, journals_papers_title_minimum_similarity, researcher)


def add_papers_different_titles(paper, papers_list, title_minimum_similarity, researcher):
    """For each paper in the researcher's paper list, checks if it's the same by doing the lcs with the titles
    and adds it if the list doesn't have the paper"""
    already_added = False
    for researcher_paper in papers_list:
        if get_similarity(paper.title.lower(),
                          researcher_paper.title.lower()) >= title_minimum_similarity:
            already_added = True
            break

    if not already_added:
        papers_list.append(paper)
        log_unify(paper.title, researcher.id, researcher.name)
