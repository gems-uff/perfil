from os import listdir, sep
from os.path import isfile, join
from sqlalchemy import or_, and_
from database.database_manager import Researcher, Project, ResearcherProject, Affiliation
from config import project_name_minimum_similarity, projects_synonyms, affiliations_dir, normalize_project
from utils.similarity_manager import detect_similar
from utils.log import log_normalize, log_primary_key_error


def add_researcher(session, tree, google_scholar_id, lattes_id):
    """Populates the Researcher table"""
    name = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO")[0]
    last_lattes_update = str(tree.xpath("/CURRICULO-VITAE/@DATA-ATUALIZACAO")[0])
    phd = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO")[0]
    phd_defense_year = phd.get("ANO-DE-CONCLUSAO")
    phd_college = phd.get("NOME-INSTITUICAO")
    google_scholar_id = google_scholar_id
    if (last_lattes_update is not None) and (len(last_lattes_update) >= 8):
        last_lattes_update = last_lattes_update[0:2] + "/" + last_lattes_update[2:4] + "/" + last_lattes_update[4:]


    new_researcher = Researcher(name=name, last_lattes_update=last_lattes_update, phd_college=phd_college,
                                phd_defense_year=phd_defense_year, google_scholar_id=google_scholar_id,
                                lattes_id=lattes_id)
    session.add(new_researcher)
    session.flush()
    return new_researcher.id


def check_if_project_is_in_the_database(session, project_name, similarity_dict):
    """Checks if a project is already in the database by looking at it's name or it's name's synonym. If any isn't found,
    checks if there is already a project with similar name in the database"""
    # checks if the exact project name is already on the database
    if len(session.query(Project).filter(Project.name == project_name).all()) > 0: return True, project_name

    if project_name in projects_synonyms:
        if len(session.query(Project).filter(Project.name == projects_synonyms[project_name]).all()) > 0: return True, projects_synonyms[project_name]
        return False, None

    if project_name in similarity_dict: return True, similarity_dict[project_name]

    projects_database_names = [project_in_bd.name for project_in_bd in session.query(Project.name)]

    similar_text_in_db = detect_similar(project_name, projects_database_names, project_name_minimum_similarity, similarity_dict)
    if similar_text_in_db is not None: return True, similar_text_in_db

    return False, None


def add_projects(session, tree, researcher_id, similarity_dict):
    """Populates the Project and ResearcherProject table"""

    projects = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE"
                          "-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA")
    researcher = session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

    for project in projects:
        name = project.get("NOME-DO-PROJETO")
        project_already_in_the_database = check_if_project_is_in_the_database(session, name, similarity_dict)

        if (not project_already_in_the_database[0]) or (not normalize_project):
            name = projects_synonyms[name] if name in projects_synonyms and normalize_project else name
            start_year = project.get("ANO-INICIO")
            end_year = project.get("ANO-FIM")
            team = ""
            manager = ""

            for member in project.findall("EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO"):
                if member.get("FLAG-RESPONSAVEL") == "NAO":
                    team += member.get("NOME-COMPLETO") + ";"
                else:
                    manager = member.get("NOME-COMPLETO") + ";"
            team = team[:-1]
            manager = manager[:-1]

            new_project = Project(name=name, start_year=start_year, end_year=end_year, team=team, manager=manager)
            session.add(new_project)
            session.flush()

            add_one_researcher_project_relationship(new_project, researcher, session)

        else:
            name = project_already_in_the_database[1]
            project_in_db = session.query(Project).filter(Project.name == name).all()[0]
            add_one_researcher_project_relationship(project_in_db, researcher, session)
            log_normalize(project_in_db.name, researcher.id, researcher.name)


def add_researcher_project(session):
    """Updates the ResearcherProject relationship for researchers which didn't have the relationship"""

    if normalize_project:

        researchers_in_projects = session.query(Researcher, Project).filter(
            or_(Project.team.contains(Researcher.name), Project.manager.contains(Researcher.name))).all()

        for relation in researchers_in_projects:
            researcher = relation[0]
            project = relation[1]

            add_one_researcher_project_relationship(project, researcher, session)
            log_normalize(project.name, researcher.id, researcher.name)


def add_one_researcher_project_relationship(project, researcher, session):
    """Adds only one ResearcherProject relationship"""

    relationship_is_not_in_db = len(session.query(ResearcherProject).filter(
        and_(ResearcherProject.researcher_id == researcher.id, ResearcherProject.project_id == project.id)).all()) == 0

    if relationship_is_not_in_db:

        new_researcher_project = ResearcherProject(researcher_id=researcher.id, project_id=project.id)
        new_researcher_project.coordinator = True if researcher.name in project.manager else False
        session.add(new_researcher_project)


def add_affiliations(session):
    """Populates the Affiliation table using the files in the affiliation directory"""

    affiliation_files = [f for f in listdir(affiliations_dir) if isfile(join(affiliations_dir, f))]

    for file in affiliation_files:
        for researcher_name in open(affiliations_dir + sep + file).readlines():

            researcher = session.query(Researcher).filter(Researcher.name == researcher_name.replace("\n", "")).all()

            if len(researcher) > 0:
                session.add(Affiliation(researcher=researcher[0].id, year=file))
                session.flush()

