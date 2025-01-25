from sqlalchemy import and_
from config import start_year, end_year, allow_in_press, QualisLevel
from database.database_manager import Paper, JournalPaper, Journal, Membership, Project, Conference, \
    ConferencePaper, Affiliation
from database.entities.paper import PaperNature


def affiliated_researcher(researcher_id, paper_year, session):
    """filter function to get only the papers within the years which the researcher was affiliated"""
    return len(session.query(Affiliation).filter(and_(Affiliation.year == paper_year, Affiliation.researcher == researcher_id)).all()) > 0


def scope_years_paper_or_support(paper_or_support):
    """filter function to get only database objects within the years specified"""
    return (start_year <= paper_or_support.year <= end_year) or (journal_paper(paper_or_support) and allow_in_press and paper_or_support.accepted)



def scope_years_researcher_project(research_project: Membership, session):
    """filter function to get only database objects within the years specified"""
    project = session.query(Project).filter(Project.id == research_project.project_id).one()
    return project.start_year <= end_year and (project.end_year == "" or project.end_year >= start_year)

def active_researcher_project(research_project: Membership, session):
    """filter function to get only database objects without end_date"""
    project = session.query(Project).filter(Project.id == research_project.project_id).one()
    return project.end_year == ""

def completed_paper_filter(paper: Paper):
    """filter only complete papers"""
    return paper.nature == PaperNature.COMPLETE or (journal_paper(paper) and allow_in_press and paper.accepted)


def jcr_pub_filter(paper: JournalPaper):
    """filter only papers which have jcr"""
    return paper.venue.jcr  # None or 0 yield False, otherwise True


def published_journal_paper(paper: JournalPaper):
    """filter only already published papers"""
    return allow_in_press or paper.accepted is False


def accepted_journal_paper_jcr(paper: JournalPaper, session, jcr_value):
    """filter accepted papers which have jcr higher than the parameter"""
    return (session.query(Journal.jcr).filter(Journal.id == paper.venue).all()[0][0] > jcr_value) and (
                paper.accepted is True)


def qualis_level_journal(paper: JournalPaper, session, qualis_level: QualisLevel):
    """filters journal papers by a QualisLevel"""
    return paper.venue.qualis == qualis_level


def qualis_level_conference(paper: ConferencePaper, session, qualis_level: QualisLevel):
    """filters conference papers by a QualisLevel"""
    return paper.venue.qualis == qualis_level


def journal_paper(paper):
    """filters journal papers"""
    return isinstance(paper, JournalPaper)


def conference_paper(paper):
    """filters conference papers"""
    return isinstance(paper, ConferencePaper)
