from os import listdir, sep
from os.path import isfile, join
from sqlalchemy import or_, and_, func
from database.database_manager import Researcher, Project, Membership, Affiliation
from config import project_name_minimum_similarity, projects_synonyms, affiliations_dir, unify_project, areas, start_year, end_year
from database.entities.researcher import Education, EducationType
from utils.similarity_manager import detect_similar
from utils.log import log_unify, log_possible_lattes_duplication


def add_researcher(session, tree, google_scholar_id, lattes_id):
    """Populates the Researcher table"""
    name = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO")[0]
    last_lattes_update = str(tree.xpath("/CURRICULO-VITAE/@DATA-ATUALIZACAO")[0])
    phd = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO")[0]
    phd_defense_year = int(phd.get("ANO-DE-CONCLUSAO"))
    phd_college = phd.get("NOME-INSTITUICAO")
    google_scholar_id = google_scholar_id
    if (last_lattes_update is not None) and (len(last_lattes_update) >= 8):
        last_lattes_update = last_lattes_update[0:2] + "/" + last_lattes_update[2:4] + "/" + last_lattes_update[4:]


    new_researcher = Researcher(name=name, last_lattes_update=last_lattes_update, phd_college=phd_college,
                                phd_defense_year=phd_defense_year, google_scholar_id=google_scholar_id,
                                lattes_id=lattes_id)
    session.add(new_researcher)
    return new_researcher


def check_if_project_is_in_the_database(session, project_name, similarity_dict):
    """Checks if a project is already in the database by looking at it's name or it's name's synonym. If any isn't found,
    checks if there is already a project with similar name in the database"""
    # checks if the exact project name is already on the database
    if len(session.query(Project).filter(func.lower(Project.name) == func.lower(project_name)).all()) > 0: return True, project_name

    if project_name in projects_synonyms:
        if len(session.query(Project).filter(Project.name == projects_synonyms[project_name]).all()) > 0: return True, projects_synonyms[project_name]
        return False, None

    if project_name in similarity_dict: return True, similarity_dict[project_name]

    projects_database_names = [project_in_bd.name for project_in_bd in session.query(Project.name)]

    similar_text_in_db = detect_similar(project_name, projects_database_names, project_name_minimum_similarity, similarity_dict)
    if similar_text_in_db is not None: return True, similar_text_in_db

    return False, None


def add_projects(session, tree, researcher, similarity_dict):
    """Populates the Project and ResearcherProject table"""

    projects = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE"
                          "-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA")

    for project in projects:
        name = project.get("NOME-DO-PROJETO").upper()
        project_already_in_the_database = check_if_project_is_in_the_database(session, name, similarity_dict)

        # Lattes duplication
        if project_already_in_the_database[0]:
            this_researcher_projects_relationship = session.query(Membership.project_id).filter(Membership.researcher_id == researcher.id)
            this_researcher_projects_in_db = session.query(Project).filter(func.lower(Project.name) == func.lower(name), Project.id.in_(this_researcher_projects_relationship))
            for project_in_db in this_researcher_projects_in_db:
                log_possible_lattes_duplication("researcher_project", researcher.name, researcher.id, project_in_db.id, name)

        # Normalize
        if unify_project and project_already_in_the_database[0]:
            project_in_db = session.query(Project).filter(func.lower(Project.name) == func.lower(project_already_in_the_database[1])).all()[0]
            add_one_researcher_project_relationship(project_in_db, researcher, session)
            log_unify(project_in_db.name, researcher.id, researcher.name)
        else:
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

            add_one_researcher_project_relationship(new_project, researcher, session)


def add_researcher_project(session):
    """Updates the ResearcherProject relationship for researchers which didn't have the relationship"""

    if unify_project:

        researchers_in_projects = session.query(Researcher, Project).filter(
            or_(Project.team.contains(Researcher.name), Project.manager.contains(Researcher.name))).all()

        for relation in researchers_in_projects:
            researcher = relation[0]
            project = relation[1]

            add_one_researcher_project_relationship(project, researcher, session)
            log_unify(project.name, researcher.id, researcher.name)


def add_one_researcher_project_relationship(project, researcher, session):
    """Adds only one ResearcherProject relationship"""

    relationship_is_not_in_db = len(session.query(Membership).filter(
        and_(Membership.researcher_id == researcher.id, Membership.project_id == project.id)).all()) == 0

    if relationship_is_not_in_db:

        new_researcher_project = Membership(researcher_id=researcher.id, project_id=project.id)
        new_researcher_project.principal_investigator = True if researcher.name in project.manager else False
        session.add(new_researcher_project)


def add_affiliations(session):
    """Populates the Affiliation table using the files in the affiliation directory"""

    for year in range(start_year, end_year + 1):
        for researcher_name in open(affiliations_dir + sep + str(year)).read().splitlines():
            researcher = session.query(Researcher).filter(Researcher.name == researcher_name).one_or_none()

            if researcher:
                session.add(Affiliation(researcher=researcher.id, year=year))
            else:
                print(f"Affiliation of {year} has researcher {researcher_name} not found in the database.")


def add_researcher_education(session, tree, researcher):
    '''Adds dsc and postdoc education from a lattes .xml file'''
    elements = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO')
    for element in elements:
        add_education(session, EducationType.DOCTORATE, element, researcher)

    elements = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/POS-DOUTORADO')
    for element in elements:
        add_education(session, EducationType.POSTDOC, element, researcher)


def add_education(session, type, element, researcher):
    '''Creates an instance of education'''  
    course = element.get('NOME-CURSO')
    codigo_area = element.get('CODIGO-AREA-CURSO')
    area = areas.get(int(codigo_area) if codigo_area else None, codigo_area)
    institution = element.get('NOME-INSTITUICAO')
    start_date = element.get('ANO-DE-INICIO')
    end_date = element.get('ANO-DE-CONCLUSAO')
    status = element.get('STATUS-DO-CURSO')

    session.add(Education(type=type.value, course=course, area=area, institution=institution, start_date=start_date, end_date=end_date, status=status, researcher=researcher))