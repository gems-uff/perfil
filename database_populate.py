from enum import Enum
from sqlalchemy import or_, not_
from sqlalchemy.orm import Session, aliased
from config import jcr
from database.database_manager import Researcher, Conference, Journal, Paper, JournalPaper, ConferencePaper, Project, \
    Student, ResearcherProject, ResearcherStudent, Venue
from database.student import Type


class AdvisorOrCommittee(Enum):
    # Enum to help the add_students function
    ADVISOR = "DE-ORIENTACOES-CONCLUIDAS-PARA"
    COMMITTEE = "DA-PARTICIPACAO-EM-BANCA-DE"


class MasterOrPHD(Enum):
    # Enum to help the add_students function
    MASTER = "MESTRADO"
    PHD = "DOUTORADO"


def add_researcher(session, tree, google_scholar_id):
    """Populates the Researcher table"""
    name = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO")[0]
    last_lattes_update = tree.xpath("/CURRICULO-VITAE/@DATA-ATUALIZACAO")[0]
    phd = tree.xpath("/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO")[0]
    phd_defense_year = phd.get("ANO-DE-CONCLUSAO")
    phd_college = phd.get("NOME-INSTITUICAO")
    google_scholar_id = google_scholar_id

    new_researcher = Researcher(name=name, last_lattes_update=last_lattes_update, phd_college=phd_college,
                                phd_defense_year=phd_defense_year,
                                google_scholar_id=google_scholar_id)
    session.add(new_researcher)
    session.flush()
    return new_researcher.id


def get_or_create_conference(session, conference_name):
    """Get a conference or populates the Conference table"""
    conference_list = session.query(Conference).filter(Conference.name == conference_name).all()

    if len(conference_list) == 0:
        conference = Conference(name=conference_name)
        session.add(conference)
        session.flush()
        return conference.id
    else:
        return conference_list[0].id


def get_or_create_journal(session, journal_details):
    """Get a journal or populates the Journal table"""
    journal_issn = journal_details.get("ISSN")[:4] + "-" + journal_details.get("ISSN")[-4:]
    journal_list = session.query(Journal).filter(Journal.issn == journal_issn).all()

    if len(journal_list) == 0:
        journal_name = journal_details.get("TITULO-DO-PERIODICO-OU-REVISTA")
        journal_jcr = jcr[journal_issn] if journal_issn in jcr else 0
        journal = Journal(name=journal_name, issn=journal_issn, jcr=journal_jcr)
        session.add(journal)
        session.flush()
        return journal.id
    else:
        return journal_list[0].id


def add_journal_papers(session, tree, researcher_id):
    """Populates the JournalPaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO")
    papers_and_venue_id = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-ARTIGO",
                                     details_attribute="DETALHAMENTO-DO-ARTIGO", title_attribute="TITULO-DO-ARTIGO",
                                     year_attribute="ANO-DO-ARTIGO", session=session)
    researcher = session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

    for paper_id in papers_and_venue_id:
        paper = paper_id[0]
        venue_id = paper_id[1]
        if len(session.query(JournalPaper).filter(JournalPaper.title == paper.title, or_(JournalPaper.doi == paper.doi,
                                                                                         JournalPaper.doi is None)).all()) == 0:
            new_journal_paper = JournalPaper(title=paper.title, doi=paper.doi, year=paper.year,
                                             first_page=paper.first_page,
                                             last_page=paper.last_page, authors=paper.authors, venue=venue_id)
            session.flush()
            new_journal_paper.researchers.append(researcher)


def add_conference_papers(session, tree, researcher_id):
    """Populates the ConferencePaper table"""
    papers_element_list = tree.xpath("/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS")
    papers_and_venue_id = get_papers(element_list=papers_element_list, basic_data_attribute="DADOS-BASICOS-DO-TRABALHO",
                                     details_attribute="DETALHAMENTO-DO-TRABALHO", title_attribute="TITULO-DO-TRABALHO",
                                     year_attribute="ANO-DO-TRABALHO", session=session)
    researcher = session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

    for paper_id in papers_and_venue_id:
        paper = paper_id[0]
        venue_id = paper_id[1]
        if len(session.query(ConferencePaper).filter(ConferencePaper.title == paper.title,
                                                     or_(ConferencePaper.doi == paper.doi,
                                                         ConferencePaper.doi is None)).all()) == 0:
            new_conference_paper = ConferencePaper(title=paper.title, doi=paper.doi, year=paper.year,
                                                   first_page=paper.first_page,
                                                   last_page=paper.last_page, authors=paper.authors, venue=venue_id)
            session.flush()
            new_conference_paper.researchers.append(researcher)


def get_papers(element_list, basic_data_attribute, details_attribute, title_attribute, year_attribute, session):
    """Get basic information on papers from xml"""
    papers = []

    for paper in element_list:
        basic_data = paper.findall(basic_data_attribute)[0]
        paper_details = paper.findall(details_attribute)[0]
        paper_authors = paper.findall("AUTORES")

        title = basic_data.get(title_attribute)
        doi = basic_data.get("DOI") if basic_data.get("DOI") != "" else None

        year = basic_data.get(year_attribute)
        first_page = paper_details.get("PAGINA-INICIAL")
        last_page = paper_details.get("PAGINA-FINAL")
        authors = ""
        venue_id = get_or_add_paper_venue_id(session, details_attribute, paper_details)

        for author in paper_authors:
            authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
        authors = authors[:-1]

        papers.append([
            Paper(title=title, doi=doi, year=year, first_page=first_page, last_page=last_page, authors=authors),
            venue_id])

    return papers


def get_or_add_paper_venue_id(session, details_attribute, paper_details):
    if details_attribute == "DETALHAMENTO-DO-TRABALHO":
        venue_name = paper_details.get("NOME-DO-EVENTO")
        return get_or_create_conference(session, venue_name)
    else:
        return get_or_create_journal(session, paper_details)


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
                # I don't know if you can have two managers or more in a team
                if member.get("FLAG-RESPONSAVEL") == "NAO":
                    team += member.get("NOME-COMPLETO") + ";"
                else:
                    manager = member.get("NOME-COMPLETO") + ";"
            team = team[:-1]
            manager = manager[:-1]

            session.add(Project(name=name, start_year=start_year, end_year=end_year, team=team, manager=manager))


def add_students(session, tree, researcher_id):
    """Call functions to populate the Student table and the ResearcherStudent relationship"""
    students_advised = tree.xpath("/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS")[0]
    students_advised_masters = students_advised.findall("ORIENTACOES-CONCLUIDAS-PARA-MESTRADO")
    students_advised_phds = students_advised.findall("ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO")

    add_students_from_element_list(session, students_advised_masters, AdvisorOrCommittee.ADVISOR, MasterOrPHD.MASTER,
                                   researcher_id)
    add_students_from_element_list(session, students_advised_phds, AdvisorOrCommittee.ADVISOR, MasterOrPHD.PHD,
                                   researcher_id)

    students_judged = tree.xpath("/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO")[0]
    students_judged_masters = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-MESTRADO")
    students_judged_phds = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-DOUTORADO")

    add_students_from_element_list(session, students_judged_masters, AdvisorOrCommittee.COMMITTEE, MasterOrPHD.MASTER,
                                   researcher_id)
    add_students_from_element_list(session, students_judged_phds, AdvisorOrCommittee.COMMITTEE, MasterOrPHD.PHD,
                                   researcher_id)


def add_students_from_element_list(session, element_list, advisor_or_committee: AdvisorOrCommittee, master_or_phd,
                                   researcher_id):
    """Populates the Student table and call a function to populate the ResearcherStudent relationship"""
    for element in element_list:
        student = element.findall(
            "DETALHAMENTO-" + advisor_or_committee.value.upper() + "-" + master_or_phd.value.upper())[0]

        name = student.get("NOME-DO-ORIENTADO") if advisor_or_committee.value in AdvisorOrCommittee.ADVISOR.value \
            else student.get("NOME-DO-CANDIDATO")

        student_id = session.query(Student.id).filter(Student.name == name).all()
        if len(student_id) == 0:
            new_student = Student(name=name)
            session.add(new_student)
            session.flush()

            student_id = new_student.id
        elif len(student_id) == 1:
            student_id = student_id[0][0]

        add_researcher_student_from_xml(session, element, advisor_or_committee, master_or_phd, student_id,
                                        researcher_id)


def add_researcher_student_from_xml(session, element, advisor_or_committee: AdvisorOrCommittee,
                                    master_or_phd: MasterOrPHD,
                                    student_id, researcher_id):
    """Populate most of the ResearcherStudent relationship with data from the lattes xml"""
    advisor_or_committee = advisor_or_committee.value
    master_or_phd = master_or_phd.value
    new_researcher_student = ResearcherStudent(student_id=student_id, researcher_id=researcher_id)
    defence_basic_data = element.findall("DADOS-BASICOS-" + advisor_or_committee + "-" + master_or_phd)[0]

    new_researcher_student.title = defence_basic_data.get("TITULO")
    new_researcher_student.year = defence_basic_data.get("ANO")
    new_researcher_student.type = researcher_student_relationship_switch(master_or_phd, advisor_or_committee)

    if AdvisorOrCommittee.COMMITTEE.value in advisor_or_committee:
        committee = element.findall("PARTICIPANTE-BANCA")
        committee_members = ""
        for member in committee:
            committee_members += member.get("NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA") + ";"
        committee_members = committee_members[:-1]

        new_researcher_student.committee = committee_members

    if len(session.query(ResearcherStudent).filter(ResearcherStudent.student_id == new_researcher_student.student_id,
                                                   ResearcherStudent.researcher_id == new_researcher_student.researcher_id,
                                                   ResearcherStudent.type == new_researcher_student.type).all()) == 0:
        session.add(new_researcher_student)


def researcher_student_relationship_switch(degree, relation):
    # function to mimic the switch statement from other tools
    type = {
        MasterOrPHD.MASTER.value + AdvisorOrCommittee.ADVISOR.value: Type.master_advisor,
        MasterOrPHD.PHD.value + AdvisorOrCommittee.ADVISOR.value: Type.phd_advisor,
        MasterOrPHD.MASTER.value + AdvisorOrCommittee.COMMITTEE.value: Type.master_comittee,
        MasterOrPHD.PHD.value + AdvisorOrCommittee.COMMITTEE.value: Type.phd_comittee
    }
    return type[degree + relation]


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


def add_coauthor_papers(session):
    """Updates the researcher_journal_paper and researcher_conference_paper from coauthors which didn't have the
    relationship """
    # The code looks like to be duplicated, but the entities/classes/tables are different

    coauthors_and_conference_papers = session.query(Researcher, ConferencePaper).filter(
        ConferencePaper.authors.contains(Researcher.name)).all()
    for relation in coauthors_and_conference_papers:
        researcher = relation[0]
        paper = relation[1]
        if paper not in researcher.conference_papers: researcher.conference_papers.append(paper)

    coauthors_and_journal_papers = session.query(Researcher, JournalPaper).filter(
        JournalPaper.authors.contains(Researcher.name)).all()
    for relation in coauthors_and_journal_papers:
        researcher = relation[0]
        paper = relation[1]
        if paper not in researcher.journal_papers: researcher.journal_papers.append(paper)


def add_researcher_student_from_database_to_committee(session):
    """Updates the committee attribute from the ResearcherStudent table"""
    researcher_in_committee = session.query(ResearcherStudent.title, Researcher.name).filter(
        or_(ResearcherStudent.type == Type.master_comittee,
            ResearcherStudent.type == Type.phd_comittee),
        ResearcherStudent.researcher_id == Researcher.id).all()

    for relation in researcher_in_committee:
        paper_title = relation[0]
        researcher_name = relation[1]

        relationship_without_committee = session.query(ResearcherStudent).filter(
            not_(ResearcherStudent.committee.contains(researcher_name)),
            ResearcherStudent.title == paper_title).all()

        for researcher_student in relationship_without_committee:
            researcher_student.committee += researcher_name + ";"
            if len(relationship_without_committee) > 0: researcher_student.committee = researcher_student.committee[:-1]
            session.flush()
