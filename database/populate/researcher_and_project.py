from sqlalchemy import or_
from database.database_manager import Researcher, Project, ResearcherProject


def add_researcher(session, tree, google_scholar_id, lattes_id):
    """Populates the Researcher table"""
    name = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO")[0]
    last_lattes_update = tree.xpath("/CURRICULO-VITAE/@DATA-ATUALIZACAO")[0]
    phd = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO")[0]
    phd_defense_year = phd.get("ANO-DE-CONCLUSAO")
    phd_college = phd.get("NOME-INSTITUICAO")
    google_scholar_id = google_scholar_id

    new_researcher = Researcher(name=name, last_lattes_update=last_lattes_update, phd_college=phd_college,
                                phd_defense_year=phd_defense_year, google_scholar_id=google_scholar_id,
                                lattes_id=lattes_id)
    session.add(new_researcher)
    session.flush()
    return new_researcher.id


def add_projects(session, tree):
    """Populates the Project table"""
    projects = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE"
                          "-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA")

    for project in projects:
        name = project.get("NOME-DO-PROJETO")
        if len(session.query(Project).filter(Project.name == name).all()) == 0:
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

            session.add(Project(name=name, start_year=start_year, end_year=end_year, team=team, manager=manager))


def add_researcher_project(session):
    """Populates the ResearcherProject relationship"""
    researchers_in_projects = session.query(Researcher.id, Researcher.name, Project.id, Project.manager).filter(
        or_(Project.team.contains(Researcher.name), Project.manager.contains(Researcher.name))).all()

    for relation in researchers_in_projects:
        researcher_id = relation[0]
        researcher_name = relation[1]
        project_id = relation[2]
        project_manager = relation[3]

        new_researcher_project = ResearcherProject(researcher_id=researcher_id, project_id=project_id)
        new_researcher_project.coordinator = True if researcher_name in project_manager else False
        session.add(new_researcher_project)