import os
import pandas as pd
import time
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
from zipfile import ZipFile
from config import start_year, end_year, lattes_dir, researchers_file, jcr, conferences_qualis, journals_qualis
from database.database_manager import start_database, database_schema_png
from database.populate.book import add_researcher_published_books, add_researcher_published_chapters
from database.populate.other_works import add_researcher_conference_management, add_researcher_editorial_board, \
    add_researcher_patents_software
from database.populate.researcher_and_project import *
from database.populate.titles_support import add_researcher_advisements, add_researcher_committee
from database.populate.venue_and_paper import add_journal_papers, add_conference_papers, add_coauthor_papers
from utils.dict_xlsx_utils import create_empty_similarity_dict, create_similarity_file

conferences_similarity_dict = None
journals_similarity_dict = None


def lattes(id, session, google_scholar_id):
    """Populates the database with the lattes info"""
    with ZipFile(lattes_dir + os.sep + str(id) + '.zip') as zip:
        with zip.open('curriculo.xml') as file:
            tree = etree.parse(file)

            researcher_id = add_researcher(session, tree, google_scholar_id)
            add_conference_papers(session, tree, researcher_id, conferences_similarity_dict)
            add_journal_papers(session, tree, researcher_id, journals_similarity_dict)
            add_projects(session, tree)
            add_researcher_advisements(session, tree, researcher_id)
            add_researcher_committee(session, tree, researcher_id)
            add_researcher_conference_management(session, tree, researcher_id)
            add_researcher_editorial_board(session, tree, researcher_id)
            add_researcher_published_books(session, tree, researcher_id)
            add_researcher_published_chapters(session, tree, researcher_id)
            add_researcher_patents_software(session, tree, researcher_id)


def update_database_info(session):
    """Updates some informations and relationships after the database is fully populated with all the lattes"""
    add_researcher_project(session)
    add_coauthor_papers(session)


def scholar(id):
    """Collects the following metrics from Google Scholar:
    - Citações *
    - H-Index
    * Collects the lifetime value appended with '(total)' and the value according to a predefined horizon.

    Keyword arguments:
    id -- the 12-character code associated with a Google Scholar profile
    """
    profile = {}
    url = 'https://scholar.google.com/citations?user=' + str(id)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    indexes = soup.find_all("td", "gsc_rsb_std")
    profile['Citações (total)'] = int(indexes[0].string)
    profile['H-Index (total)'] = int(indexes[2].string)

    citations = soup.find_all("span", "gsc_g_al")
    sum = 0
    current_year = datetime.now().year
    for i in range(-(current_year - end_year + 1), -(min(current_year - start_year + 1, len(citations)) + 1), -1):
        try:
            sum += int(citations[i].string)
        except:
            pass
    profile['Citações'] = sum

    return profile


# def all(id_lattes, id_scholar):
#     """Collects all metrics of a given researcher.
#     Please cheque the metric list in the documentation of functions lattes, scholar, and normalized.
#
#     Keyword arguments:
#     id_lattes -- the 16-digit number associated with a Lattes CV
#     id_scholar -- the 12-character code associated with a Google Scholar profile
#     """
#     lattes(id_lattes)
#     # profile.update(scholar(id_scholar))
#     # return profile


def initialize_similarities_dict():
    """Initialize the similarities dict using the qualis dicts keys"""
    global conferences_similarity_dict
    conferences_similarity_dict = create_empty_similarity_dict(conferences_qualis)
    global journals_similarity_dict
    journals_similarity_dict = create_empty_similarity_dict(journals_qualis)


def create_similarities_xlsx():
    """Creates .xlsx from the similarities dictionaries"""
    create_similarity_file(conferences_similarity_dict, "conferences_similar")
    create_similarity_file(journals_similarity_dict, "journals_similar")


def main():
    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})
    initialize_similarities_dict()
    max = len(df)
    print('Processing', max, 'researchers...\n')
    # database_schema_png()
    session = start_database(False)

    for i, row in df.iterrows():
        profile = row.to_dict()
        print(profile['Nome'] + '...')
        if not pd.isnull(profile['ID Lattes']):
            lattes(profile['ID Lattes'], session, profile['ID Scholar'])
        if not pd.isnull(profile['ID Scholar']):
            try:
                profile.update(scholar(profile['ID Scholar']))
            except:
                print(f"Failed to retrieve Google Scholar data.")

        # for key, value in profile.items():
        # df.at[i, key] = value  TODO check erro
        print('\tOk ({:.0f}%).'.format((i + 1) / max * 100))
        if not (i + 1) % 5:
            print('\nPausing for 10 seconds to avoid Google Scholar complaining...\n')
            time.sleep(10)

    print("\nFinished.")
    update_database_info(session)

    df.to_excel(researchers_file, index=False)
    create_similarities_xlsx()
    return session


if __name__ == "__main__":
    main()
