from config import start_year, end_year
from database.database_manager import Paper, JournalPaper, Journal, ResearcherProject, Project
from database.entities.paper import PaperNature


def scope_years_paper_or_support(paper_or_support):
    """filter function to get only database objects within the years specified"""
    return (start_year <= paper_or_support.year <= end_year)


def scope_years_researcher_project(research_project: ResearcherProject, session):
    """filter function to get only database objects within the years specified"""
    return start_year <= session.query(Project.start_year).filter(Project.id == research_project.project_id).all()[0][
        0] <= end_year


def completed_paper_filter(paper: Paper):
    """filter only complete papers"""
    return paper.nature == PaperNature.COMPLETE


def jcr_pub_filter(paper: JournalPaper, session, jcr_value):
    """filter only already published, complete papers which have jcr higher than the parameter"""
    return (session.query(Journal.jcr).filter(Journal.id == paper.venue).all()[0][0] > jcr_value) and (
            paper.nature == PaperNature.COMPLETE) and (paper.accepted is False)


def published_journal_paper(paper: JournalPaper):
    """filter only already published papers"""
    return paper.accepted is False


def accepted_journal_paper_jcr(paper: JournalPaper, session, jcr_value):
    """filter accepted papers which have jcr higher than the parameter"""
    return (session.query(Journal.jcr).filter(Journal.id == paper.venue).all()[0][0] > jcr_value) and (paper.accepted is True)

