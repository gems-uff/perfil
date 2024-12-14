import os
import pandas as pd
from lxml import etree
from zipfile import ZipFile
from config import lattes_dir, researchers_file, similarity_dir
from database.database_manager import start_database
from database.populate.book import add_researcher_published_books, add_researcher_published_chapters
from database.populate.other_works import add_researcher_conference_management, add_researcher_editorial_board, \
    add_researcher_patents_software
from database.populate.researcher_and_project import *
from database.populate.titles_support import add_researcher_advisements, add_researcher_committees
from database.populate.venue_and_paper import add_journal_papers, add_conference_papers, add_coauthor_papers
from utils.dict_xlsx_utils import write_dict

conferences_similarity_dict = dict()
journals_similarity_dict = dict()
project_similarity_dict = dict()


def lattes(lattes_id, session, google_scholar_id):
    """Populates the database with the lattes info"""
    with ZipFile(lattes_dir + os.sep + str(lattes_id) + '.zip') as zip:
        with zip.open('curriculo.xml') as file:
            tree = etree.parse(file)

            researcher_id = add_researcher(session, tree, google_scholar_id, lattes_id)
            add_conference_papers(session, tree, researcher_id, conferences_similarity_dict)
            add_journal_papers(session, tree, researcher_id, journals_similarity_dict)
            add_projects(session, tree, researcher_id, project_similarity_dict)
            add_researcher_advisements(session, tree, researcher_id)
            add_researcher_committees(session, tree, researcher_id)
            add_researcher_conference_management(session, tree, researcher_id)
            add_researcher_editorial_board(session, tree, researcher_id)
            add_researcher_published_books(session, tree, researcher_id)
            add_researcher_published_chapters(session, tree, researcher_id)
            add_researcher_patents_software(session, tree, researcher_id)


def update_database_info(session):
    """Updates some informations and relationships after the database is fully populated with all the lattes"""
    add_researcher_project(session)
    add_coauthor_papers(session)
    add_affiliations(session)


def create_similarities_xlsx():
    """Creates .xlsx from the similarities dictionaries"""
    write_dict(project_similarity_dict, similarity_dir + os.sep + "projects_similar")
    write_dict(conferences_similarity_dict, similarity_dir+os.sep+"conferences_similar")
    write_dict(journals_similarity_dict, similarity_dir+os.sep+"journals_similar")


def main(one_researcher_profile = None):
    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})
    max = len(df) if one_researcher_profile is None else 1
    print('Processing', max, 'researchers...\n')
    # database_schema_png()
    session = start_database(False)

    for i, row in df.iterrows():
        profile = row.to_dict() if one_researcher_profile == None else one_researcher_profile
        print(profile['Nome'] + '...')
        if not pd.isnull(profile['ID Lattes']):
            lattes(profile['ID Lattes'], session, profile['ID Scholar'])
            if one_researcher_profile is not None: break

        print('\tOk ({:.0f}%).'.format((i + 1) / max * 100))

    update_database_info(session)
    print("\nFinished populating the database. \n")

    create_similarities_xlsx()
    return session


if __name__ == "__main__":
    main()
