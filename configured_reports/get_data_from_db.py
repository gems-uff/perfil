from sqlalchemy import and_
from config import start_year, end_year
from database.entities.book import ResearcherPublishedBook, PublishedBook, ResearcherPublishedBookChapter, \
    PublishedBookChapter
from database.entities.other_works import ResearcherPatent, Patent, ResearcherConferenceManagement, \
    ResearcherEditorialBoard
from database.entities.project import ResearcherProject, Project
from database.entities.researcher import Researcher
from database.entities.titles_support import ResearcherAdvisement, ResearcherCommittee, CommitteeTypes
from database.entities.venue import Venue
from utils.list_filters import scope_years_paper_or_support
from utils.xlsx_utils import calculate_number_of_pages, get_qualis_points
from configured_reports.util import append_lists


def get_researchers(researcher_id, session):
    """Returns a list with one researcher if researcher_id <= 0, otherwise returns a list with all researchers"""

    return session.query(Researcher).all() if researcher_id <= 0 else session.query(Researcher).filter(
        Researcher.id == researcher_id).all()


def quantity_of_researcher_itens(session, item_class: str, researcher_id):
    """Returns the quantity of times a researchers needs to be repeated accordingly with the item_class variable
    received"""

    researcher_itens = {
        "Artigo": append_lists(get_paper_list(session, False, researcher_id), get_paper_list(session, True, researcher_id)),
        "Banca": get_committee_list(session, researcher_id),
        "Capitulo": get_published_book_chapter_list(session, researcher_id),
        "Conferencia": get_paper_list(session, False, researcher_id),
        "Corpo_Editorial": get_editorial_board_list(session, researcher_id),
        "Livro": get_published_book_list(session, researcher_id),
        "Organizao_Evento": get_conference_management_list(session, researcher_id),
        "Orientacao": get_advisement_list(session, researcher_id),
        "Patente": get_patent_list(session, researcher_id),
        "Periodico": get_paper_list(session, True, researcher_id),
        "Projeto": get_project_list(session, researcher_id)
    }

    return len(researcher_itens[item_class])


def get_researchers_list(session, cartesian_product: bool, item_class):
    """Returns the list of researchers repeated as many time is necessary accordingly with the parameters received"""

    researchers = session.query(Researcher).all()

    if cartesian_product:
        researchers_list = []
        for researcher in researchers:
            for i in range(quantity_of_researcher_itens(session, item_class, researcher.id)): researchers_list.append(researcher)
        return researchers_list

    return researchers


def get_paper_list(session, is_journal: bool, researcher_id=0):
    """Returns the list of papers be it journal papers or conference papers of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    paper_list = []

    for researcher in researchers:
        papers = list(filter(scope_years_paper_or_support, researcher.journal_papers)) if is_journal else \
            list(filter(scope_years_paper_or_support, researcher.conference_papers))

        paper_list.extend(papers)

    return paper_list


def get_papers_venues_list(session, is_journal: bool, researcher_id=0):
    """Returns the list of venues of journal papers or conference papers of a given researcher or all of them"""

    papers = get_paper_list(session, is_journal, researcher_id)
    venues_ids = [paper.venue for paper in papers]
    venue_list = []

    for venue_id in venues_ids:
        venue_list.append(session.query(Venue).filter(Venue.id == venue_id).all()[0])

    return venue_list


def get_advisement_list(session, researcher_id=0):
    """Return the advisements list of a given researcher or all of them"""

    researcher_list = get_researchers(researcher_id, session)
    advisement_list = []
    for researcher in researcher_list:
        advisement_list.append(session.query(ResearcherAdvisement).filter(ResearcherAdvisement.researcher_id == researcher.id).all()[0])
    return list(filter(scope_years_paper_or_support, advisement_list))


def get_committee_list(session, researcher_id=0):
    """Returns the committees list of a given researcher or all of them"""

    researcher_list = get_researchers(researcher_id, session)
    committee_list = []
    for researcher in researcher_list:
        committee_list.append(session.query(ResearcherCommittee).filter(ResearcherCommittee.researcher_id == researcher.id).all()[0])
    return list(filter(scope_years_paper_or_support, committee_list))


def get_patent_list(session, researcher_id=0):
    """Returns the patent list of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    patent_list = []

    # to make sure the order is by researcher
    for researcher in researchers:
        relationship = session.query(ResearcherPatent).filter(ResearcherPatent.researcher_id == researcher.id).all()
        for patent_relationship in relationship:
            patent = session.query(Patent).filter(Patent.id == patent_relationship.patent_id).all()[0]
            if start_year <= patent.year <= end_year: patent_list.append(patent)

    return patent_list


def get_conference_management_list(session, researcher_id=0):
    """Returns the conference management list of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    conference_management_list = []

    for researcher in researchers:
        conference_management_list.extend(session.query(ResearcherConferenceManagement)
            .filter(and_(ResearcherConferenceManagement.researcher_id == researcher.id,
                         start_year <= ResearcherConferenceManagement.year, ResearcherConferenceManagement.year <= end_year)).all())

    return conference_management_list


def get_editorial_board_list(session, researcher_id=0):
    """Returns the editorial board list of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    editorial_board_list = []

    for researcher in researchers:
        editorial_board_list.extend(session.query(ResearcherEditorialBoard)
            .filter(and_(ResearcherEditorialBoard.researcher_id == researcher.id,
                         start_year <= ResearcherEditorialBoard.start_year, ResearcherEditorialBoard.start_year <= end_year)).all())

    return editorial_board_list


def get_researcher_project_or_project_lists(session, get_projects: bool, researcher_id=0):
    """Return the project list or research_project relationship list of a given researcher or all of them"""

    researcher_list = get_researchers(researcher_id, session)
    researcher_project_list = []
    project_list = []

    # to make sure the order is by researcher
    for researcher in researcher_list:
        relationship = session.query(ResearcherProject).filter(ResearcherProject.researcher_id == researcher.id).all()

        # getting only the relationships or projects between the scope years
        for researcher_project in relationship:
            project = session.query(Project).filter(Project.id == researcher_project.project_id).all()[0]
            if start_year <= project.start_year <= end_year:
                if get_projects: project_list.append(project)
                else: researcher_project_list.append(researcher_project)

    return project_list if get_projects else researcher_project_list


def get_project_list(session, researcher_id=0):
    """Returns the project list of a given researcher or all of them"""

    return get_researcher_project_or_project_lists(session, True, researcher_id)


def get_researcher_project_list(session, researcher_id=0):
    """Returns the researche_project relationship list of a given researcher or all of them"""

    return get_researcher_project_or_project_lists(session, False, researcher_id)


def get_published_book_list(session, researcher_id=0):
    """Return the published book list of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    published_book_list = []

    for researcher in researchers:
        relationship = session.query(ResearcherPublishedBook).filter(ResearcherPublishedBook.researcher_id == researcher.id).all()
        for published_book in relationship:
            book = session.query(PublishedBook).filter(PublishedBook.id == published_book.published_book_id).all()[0]
            if start_year <= book.year <= end_year: published_book_list.append(book)

    return published_book_list


def get_published_book_chapter_list(session, researcher_id=0):
    """Returns the published chapter list of a given researcher or all of them"""

    researchers = get_researchers(researcher_id, session)
    published_book_chapter_list = []

    for researcher in researchers:
        relationship = session.query(ResearcherPublishedBookChapter).filter(
            ResearcherPublishedBookChapter.researcher_id == researcher.id).all()
        for published_book_chapter in relationship:
            chapter = session.query(PublishedBookChapter).filter(PublishedBookChapter.id == published_book_chapter.published_book_chapter_id).all()[0]
            if start_year <= chapter.year <= end_year: published_book_chapter_list.append(chapter)

    return published_book_chapter_list