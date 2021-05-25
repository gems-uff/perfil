import os
import pandas as pd
import time
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
from zipfile import ZipFile

from config import start_year, end_year, lattes_dir, researchers_file, jcr
from database.database_manager import start_database, database_schema_png
from database_populate import *


def lattes(id, session, google_scholar_id):
    """Populates the database with the lattes info"""
    with ZipFile(lattes_dir + os.sep + str(id) + '.zip') as zip:
        with zip.open('curriculo.xml') as file:
            tree = etree.parse(file)

            researcher_id = add_researcher(session, tree, google_scholar_id)
            add_conference_papers(session, tree, researcher_id)
            add_journal_papers(session, tree, researcher_id)
            add_projects(session, tree)
            add_students(session, tree, researcher_id)


def update_database_info(session):
    """Updates some informations and relationships after the database is fully populated with all the lattes"""
    add_researcher_project(session)
    add_coauthor_papers(session)
    add_researcher_student_from_database_to_committee(session)


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


def all(id_lattes, id_scholar):
    """Collects all metrics of a given researcher.
    Please cheque the metric list in the documentation of functions lattes, scholar, and normalized.

    Keyword arguments:
    id_lattes -- the 16-digit number associated with a Lattes CV
    id_scholar -- the 12-character code associated with a Google Scholar profile
    """
    lattes(id_lattes)
    profile.update(scholar(id_scholar))
    return profile


def main():
    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    max = len(df)
    print('Processing', max, 'researchers...\n')

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

        # print(profile) #testing

    print("\nFinished.")
    update_database_info(session)
    test_database(session)

    df.to_excel(researchers_file, index=False)


if __name__ == "__main__":
    main()
