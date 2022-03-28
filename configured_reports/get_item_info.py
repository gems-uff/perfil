from database.entities.researcher import Researcher
from database.entities.titles_support import CommitteeTypes
from configured_reports.get_data_from_db import get_paper_list, get_papers_venues_list, get_advisement_list, \
    get_committee_list, \
    get_project_list, get_researcher_project_list, get_patent_list, get_conference_management_list, \
    get_editorial_board_list, get_published_book_chapter_list, get_published_book_list, get_researchers_list
from utils.xlsx_utils import calculate_number_of_pages, get_qualis_points


def get_class_name_from_item(item):
    return item.split(".")[0] if item is not None else None


def get_researchers_names(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.name for researcher in researchers]


def get_last_lattes_update_list(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.last_lattes_update for researcher in researchers]


def get_phd_college_list(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.phd_college for researcher in researchers]


def get_phd_defense_year_list(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.phd_defense_year for researcher in researchers]


def get_google_scholar_id_list(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.google_scholar_id for researcher in researchers]


def get_lattes_id_list(session, cartesian_product):
    researchers = get_researchers_list(session, cartesian_product[0], get_class_name_from_item(cartesian_product[1]))
    return [researcher.lattes_id for researcher in researchers]


def get_paper_year_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [paper.year for paper in papers]


def get_paper_title_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [paper.title for paper in papers]


def get_venue_names_list(session, is_journal: bool):
    venues = get_papers_venues_list(session, is_journal)
    return [venue.name for venue in venues]


def get_papers_pages_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [calculate_number_of_pages(paper) for paper in papers]


def get_papers_qualis_list(session, is_journal: bool):
    venues = get_papers_venues_list(session, is_journal)
    return [(venue.qualis.value if venue.qualis is not None else "null") for venue in venues]


def get_jcr_list(session):
    venues = get_papers_venues_list(session, True)
    return [venue.jcr for venue in venues]


def get_forum_oficial_list(session, is_journal: bool):
    venues = get_papers_venues_list(session, is_journal)
    return [venue.forum_oficial for venue in venues]


def get_doi_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [("https://doi.org/" + paper.doi if paper.doi is not None else "null") for paper in papers]


def get_qualis_points_list(session, is_journal: bool):
    venues = get_papers_venues_list(session, is_journal)
    return [get_qualis_points(is_journal, venue.qualis) if venue.qualis is not None else "null" for venue in venues]


def get_authors_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [paper.authors for paper in papers]


def get_issn_list(session):
    venues = get_papers_venues_list(session, True)
    return [venue.issn for venue in venues]


def get_paper_nature_list(session, is_journal: bool):
    papers = get_paper_list(session, is_journal)
    return [(paper.nature.value if paper.nature is not None else "null") for paper in papers]


def get_journal_accepted_list(session):
    papers = get_paper_list(session, True)
    return [("Sim" if paper.accepted else "Não") for paper in papers]


def get_conference_acronym_list(session):
    venues = get_papers_venues_list(session, False)
    return [(venue.acronym if venue.acronym is not None else "null") for venue in venues]


def get_advisement_student_list(session):
    advisements = get_advisement_list(session)
    return [advisement.student_name for advisement in advisements]


def get_advisement_college_list(session):
    advisements = get_advisement_list(session)
    return [advisement.college for advisement in advisements]


def get_advisement_year_list(session):
    advisements = get_advisement_list(session)
    return [advisement.year for advisement in advisements]


def get_advisement_title_list(session):
    advisements = get_advisement_list(session)
    return [advisement.title for advisement in advisements]


def get_advisement_type_list(session):
    advisements = get_advisement_list(session)
    return [(advisement.type.value if advisement.type is not None else "null") for advisement in advisements]


def get_committee_student_list(session):
    committees = get_committee_list(session)
    return [committee.student_name if committee.type is not CommitteeTypes.CIVIL_SERVICE_EXAMINATION
            else committee.title for committee in committees]


def get_committee_college_list(session):
    committees = get_committee_list(session)
    return [committee.college for committee in committees]


def get_committee_year_list(session):
    committees = get_committee_list(session)
    return [committee.year for committee in committees]


def get_committee_title_list(session):
    committees = get_committee_list(session)
    return [committee.title for committee in committees]


def get_committee_type_list(session):
    committees = get_committee_list(session)
    return [(committee.type.value if committee.type is not None else "null") for committee in committees]


def get_committee_team(session):
    committees = get_committee_list(session)
    return [committee.team for committee in committees]


def get_project_name_list(session):
    projects = get_project_list(session)
    return [project.name for project in projects]


def get_project_manager_list(session):
    projects = get_project_list(session)
    return [project.manager for project in projects]


def get_project_coordinator_list(session):
    project_researcher_list = get_researcher_project_list(session)
    return [("Sim" if project_researcher.coordinator else "Não") for project_researcher in project_researcher_list]


def get_project_team_list(session):
    projects = get_project_list(session)
    return [(project.team if project.team != "" else "null") for project in projects]


def get_project_start_year_list(session):
    projects = get_project_list(session)
    return [project.start_year for project in projects]


def get_project_end_year_list(session):
    projects = get_project_list(session)
    return [(project.end_year if project.end_year != "" else "null") for project in projects]


def get_patent_type_list(session):
    patents = get_patent_list(session)
    return [patent.type.value for patent in patents]


def get_patent_title_list(session):
    patents = get_patent_list(session)
    return [patent.title for patent in patents]


def get_patent_authors_list(session):
    patents = get_patent_list(session)
    return [patent.authors if patent.authors != "" else "null" for patent in patents]


def get_patent_local_list(session):
    patents = get_patent_list(session)
    return [patent.local_of_registry for patent in patents]


def get_patent_number_list(session):
    patents = get_patent_list(session)
    return [patent.number for patent in patents]


def get_patent_year_list(session):
    patents = get_patent_list(session)
    return [patent.year for patent in patents]


def get_conference_management_title_list(session):
    conferences_management = get_conference_management_list(session)
    return [job.title for job in conferences_management]


def get_conference_management_year_list(session):
    conferences_management = get_conference_management_list(session)
    return [job.year for job in conferences_management]


def get_conference_management_committee_list(session):
    conferences_management = get_conference_management_list(session)
    return [job.committee for job in conferences_management]


def get_editorial_board_journal_name_list(session):
    editorial_boards = get_editorial_board_list(session)
    return [job.journal_name for job in editorial_boards]


def get_editorial_board_type_list(session):
    editorial_boards = get_editorial_board_list(session)
    return [job.type.value for job in editorial_boards]


def get_editorial_board_start_year_list(session):
    editorial_boards = get_editorial_board_list(session)
    return [job.start_year for job in editorial_boards]


def get_editorial_board_end_year_list(session):
    editorial_boards = get_editorial_board_list(session)
    return [job.end_year if job.end_year != "" else "null" for job in editorial_boards]


def get_book_title_list(session, is_chapter: bool):
    books = get_published_book_chapter_list(session) if is_chapter else get_published_book_list(session)
    return [book.title for book in books]


def get_book_publisher_list(session, is_chapter: bool):
    books = get_published_book_chapter_list(session) if is_chapter else get_published_book_list(session)
    return [book.publisher for book in books]


def get_book_year_list(session, is_chapter: bool):
    books = get_published_book_chapter_list(session) if is_chapter else get_published_book_list(session)
    return [book.year for book in books]


def get_book_authors_list(session, is_chapter: bool):
    books = get_published_book_chapter_list(session) if is_chapter else get_published_book_list(session)
    return [book.authors for book in books]


def get_chapter_title_list(session):
    chapters = get_published_book_chapter_list(session)
    return [chapter.chapter_title for chapter in chapters]