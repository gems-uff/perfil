import time
import urllib.request
import pandas as pd
from sqlalchemy import and_
from datetime import datetime
from bs4 import BeautifulSoup
from config import start_year, end_year, researchers_file, skip_scholar
from database.database_manager import Researcher, Membership, Advisement, Committee
from database.entities.titles_support import AdvisementsTypes, CommitteeTypes
import populate_database
from utils.list_filters import active_researcher_project, completed_paper_filter, jcr_pub_filter, scope_years_paper_or_support, \
    scope_years_researcher_project, published_journal_paper, accepted_journal_paper_jcr


def lattes_full(completed_and_published_journal_papers, completed_conference_papers, masters_advisement,
                masters_committee, papers_with_jcr, phd_advisement, phd_committee,
                profile, projects_coordinated, projects_participated):
    """Populates the profile dictionary with information from all years"""

    new_profile = profile

    new_profile['Participações em Projetos (total)'] = len(projects_participated)
    new_profile['Projetos Coordenados (total)'] = len(projects_coordinated)
    new_profile['Projetos (total)'] = new_profile['Participações em Projetos (total)'] + new_profile['Projetos Coordenados (total)']

    new_profile['Orientações de Mestrado (total)'] = len(masters_advisement)
    new_profile['Orientações de Doutorado (total)'] = len(phd_advisement)
    new_profile['Orientações (total)'] = new_profile['Orientações de Mestrado (total)'] + new_profile['Orientações de Doutorado (total)']

    new_profile['Bancas de Mestrado (total)'] = len(masters_committee)
    new_profile['Bancas de Doutorado (total)'] = len(phd_committee)
    new_profile['Bancas (total)'] = new_profile['Bancas de Mestrado (total)'] + new_profile['Bancas de Doutorado (total)']

    new_profile['Publicações em Congressos (total)'] = len(completed_conference_papers)
    new_profile['Publicações em Periódicos (total)'] = len(completed_and_published_journal_papers)
    new_profile['Publicações (total)'] = new_profile['Publicações em Congressos (total)'] + new_profile['Publicações em Periódicos (total)']

    new_profile['Publicações JCR (total)'] = len(papers_with_jcr)

    return new_profile


def lattes_scope_years(completed_and_published_journal_papers, completed_conference_papers, masters_advisement,
                       masters_committee, papers_with_jcr, phd_advisement,
                       phd_committee, profile, projects_coordinated, projects_participated, researcher, session):
    """Populates the profile dictionary with information only within the years specified in config.py"""

    new_profile = profile

    new_profile['Participações em Projetos'] = len(list(filter(lambda x: scope_years_researcher_project(x, session), projects_participated)))
    new_profile['Projetos Coordenados'] = len(list(filter(lambda x: scope_years_researcher_project(x, session), projects_coordinated)))
    new_profile['Projetos Vigentes'] = len(list(filter(lambda x: active_researcher_project(x, session), projects_participated + projects_coordinated)))
    new_profile['Projetos'] = new_profile['Participações em Projetos'] + new_profile['Projetos Coordenados']

    new_profile['Orientações de Mestrado'] = len(list(filter(scope_years_paper_or_support, masters_advisement)))
    new_profile['Orientações de Doutorado'] = len(list(filter(scope_years_paper_or_support, phd_advisement)))
    new_profile['Orientações'] = new_profile['Orientações de Mestrado'] + new_profile['Orientações de Doutorado']

    new_profile['Bancas de Mestrado'] = len(list(filter(scope_years_paper_or_support, masters_committee)))
    new_profile['Bancas de Doutorado'] = len(list(filter(scope_years_paper_or_support, phd_committee)))
    new_profile['Bancas'] = new_profile['Bancas de Mestrado'] + new_profile['Bancas de Doutorado']

    new_profile['Publicações em Congressos'] = len(list(filter(scope_years_paper_or_support, completed_conference_papers)))
    new_profile['Publicações em Periódicos'] = len(list(filter(scope_years_paper_or_support, completed_and_published_journal_papers)))
    new_profile['Publicações'] = new_profile['Publicações em Congressos'] + new_profile['Publicações em Periódicos']

    new_profile['Publicações JCR'] = len(list(filter(scope_years_paper_or_support, papers_with_jcr)))

    return new_profile


def lattes(researcher, session):
    """Creates a profile dictionary and populates it with basic information about the researcher and calls functions to
    populate it with more specific information"""
    masters_advisement = session.query(Advisement).filter(
        and_(Advisement.researcher_id == researcher.id,
             Advisement.type == AdvisementsTypes.MASTER)).all()
    phd_advisement = session.query(Advisement).filter(
        and_(Advisement.researcher_id == researcher.id,
             Advisement.type == AdvisementsTypes.PHD)).all()
    masters_committee = session.query(Committee).filter(
        and_(Committee.researcher_id == researcher.id,
             Committee.type == CommitteeTypes.MASTER)).all()
    phd_committee = session.query(Committee).filter(and_(Committee.researcher_id == researcher.id,
                                                         Committee.type == CommitteeTypes.PHD)).all()
    projects_participated = session.query(Membership).filter(
        and_(Membership.researcher_id == researcher.id,
             Membership.principal_investigator == False)).all()
    projects_coordinated = session.query(Membership).filter(
        and_(Membership.researcher_id == researcher.id,
             Membership.principal_investigator == True)).all()

    completed_conference_papers = list(filter(completed_paper_filter, researcher.conference_papers))

    completed_journal_papers = list(filter(completed_paper_filter, researcher.journal_papers))
    completed_and_published_journal_papers = list(filter(published_journal_paper, completed_journal_papers))

    papers_with_jcr = list(filter(lambda x: jcr_pub_filter(x), researcher.journal_papers))

    profile = {}

    profile['Nome'] = researcher.name
    profile['Ano do Doutorado'] = researcher.phd_defense_year if researcher.phd_defense_year > 0 else '--'
    profile['Idade Acadêmica'] = datetime.now().year - researcher.phd_defense_year if researcher.phd_defense_year > 0 else 0

    profile = lattes_full(completed_and_published_journal_papers, completed_conference_papers, masters_advisement,
                masters_committee, papers_with_jcr, phd_advisement, phd_committee,
                profile, projects_coordinated, projects_participated)

    profile = lattes_scope_years(completed_and_published_journal_papers, completed_conference_papers, masters_advisement,
                       masters_committee, papers_with_jcr, phd_advisement,
                       phd_committee, profile, projects_coordinated, projects_participated, researcher, session)

    return profile


def scholar(researcher):
    """Collects the following metrics from Google Scholar:
    - Citações *
    - H-Index
    * Collects the lifetime value appended with '(total)' and the value according to a predefined horizon.

    Keyword arguments:
    id -- the 12-character code associated with a Google Scholar profile
    """

    google_scholar_id = researcher.google_scholar_id
    profile = {}

    if google_scholar_id is not None and google_scholar_id.strip() != "":

        try:
            url = 'https://scholar.google.com/citations?user=' + str(google_scholar_id)
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            indexes = soup.find_all("td", "gsc_rsb_std")
            profile['Citações (total)'] = int(indexes[0].string)
            profile['H-Index (total)'] = int(indexes[2].string)

            citations = soup.find_all("span", "gsc_g_al")
        except:
            print("Erro while trying to get " + researcher.name + "'s Google Scholar info")
            return profile

        sum = 0
        current_year = datetime.now().year
        for i in range(-(current_year - end_year + 1), -(min(current_year - start_year + 1, len(citations)) + 1), -1):
            try:
                sum += int(citations[i].string)
            except:
                pass
        profile['Citações'] = sum

    return profile


def normalized(profile):
    """Tries to generate the following normalized metrics considering the academic age (years since the PhD defense) of the researcher, appended with (anual):
    - Participações em Projetos
    - Projetos Coordenados
    - Projetos
    - Orientações de Mestrado
    - Orientações de Doutorado
    - Orientações
    - Bancas de Mestrado
    - Bancas de Doutorado
    - Bancas
    - Publicações em Congressos
    - Publicações em Periódicos
    - Publicações JCR
    - Publicações
    - Citações
    - H-Index
    Please, call lattes and scholar (optional) before calling this function.

    Keyword arguments:
    profile -- a dictionary with all metrics previously collected by lattes and scholar functions
    """
    if 'Idade Acadêmica' not in profile:
        raise RuntimeError('Please call the lattes function before using the normalized function.')

    normalized = {}
    metrics = ['Participações em Projetos', 'Projetos Coordenados', 'Projetos', 'Orientações de Mestrado',
               'Orientações de Doutorado', 'Orientações', 'Bancas de Mestrado', 'Bancas de Doutorado', 'Bancas',
               'Publicações em Congressos', 'Publicações em Periódicos', 'Publicações JCR', 'Publicações', 'Citações',
               'H-Index']
    for metric in metrics:
        metric_total = metric + ' (total)'
        if metric_total in profile and profile['Idade Acadêmica'] > 0:
            normalized[metric + ' (anual)'] = profile[metric_total] / profile['Idade Acadêmica']

    return normalized


def generate_researcher_profile_dict(researcher: Researcher, session):
    """Generates and populates the profile dictionary of a researcher"""
    profile = lattes(researcher, session)
    if not skip_scholar:
        profile.update(scholar(researcher))
    profile.update(normalized(profile))

    return profile


def main():
    session = populate_database.main()
    researchers = session.query(Researcher).all()

    print("\nStarting to write the profile(s)")

    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})
    researcher_count = 1
    for researcher in researchers:
        if not skip_scholar and not researcher_count % 6:
            print('\nPausing for 10 seconds to avoid Google Scholar complaining...\n')
            time.sleep(10)
        profile = generate_researcher_profile_dict(researcher, session)
        print('{:.0f}%...'.format((researcher_count) / len(researchers) * 100), end="", flush=True)
        for key, value in profile.items():
            df.at[researcher_count-1, key] = value

        researcher_count += 1

    df.to_excel(researchers_file, index=False)

    print("\nFinished writing the profile(s)")


if __name__ == "__main__":
    main()
