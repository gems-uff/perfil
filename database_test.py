import unittest
from lxml import etree
from database.database_manager import start_database
from database_populate import *


class DatabaseTestCase(unittest.TestCase):
    session = None
    tree = None
    google_scholar_id = "VEbJeB8AAAAJ"
    researcher_id = 1

    @classmethod
    def setUpClass(cls):
        """Initialize some attributes to make the tests"""
        cls.session = start_database(False)
        with open("curriculo_test.xml", encoding="ISO-8859-1") as file:
            cls.tree = etree.parse(file)

    def test1AddResearcher(self):
        """Adds the researcher which will be used in most of the tests"""
        researcher_id = add_researcher(self.session, self.tree, self.google_scholar_id)
        researcher_database = self.session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

        self.assertEqual(researcher_database.name, "Leonardo Gresta Paulino Murta")
        self.assertEqual(researcher_database.last_lattes_update, "20012021")
        self.assertEqual(researcher_database.phd_college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(researcher_database.phd_defense_year, 2006)

    def test2AddJournalPapers(self):
        """Adds the reseacher journal papers and checks if all the information and realtionships with
        venues are correct"""
        add_journal_papers(session=self.session, tree=self.tree, researcher_id=self.researcher_id)
        journals_papers_database = self.session.query(JournalPaper).all()

        journal_paper_one, journal_paper_two = journals_papers_database[0], journals_papers_database[1]
        journal_one = self.session.query(Journal).filter(Journal.id == journal_paper_one.venue).all()[0]
        journal_two = self.session.query(Journal).filter(Journal.id == journal_paper_two.venue).all()[0]

        # JournalPapers
        # one
        self.assertEqual(journal_paper_one.researchers[0].id, 1)
        self.assertEqual(journal_paper_one.title, "A Caminho da Manuten\xC3\xA7\xC3\xA3o de Software Baseada em "
                                                  "Componentes via T\xC3\xA9cnicas de Ger\xC3\xAAncia de "
                                                  "Configura\xC3\xA7\xC3\xA3o de Software")
        self.assertEqual(journal_paper_one.doi, None)
        self.assertEqual(journal_paper_one.year, 2005)
        self.assertEqual(journal_paper_one.first_page, 45)
        self.assertEqual(journal_paper_one.last_page, 62)
        self.assertEqual(journal_paper_one.authors, "Leonardo Gresta Paulino Murta;Cristine Ribeiro Dantas;Hamilton "
                                                    "Oliveira;Luiz Gustavo Berno Lopes;Cl\xC3\xA1udia Maria Lima "
                                                    "Werner")
        # two
        self.assertEqual(journal_paper_two.researchers[0].id, 1)
        self.assertEqual(journal_paper_two.title, "Odyssey-SCM: An Integrated Software Configuration Management "
                                                  "Infrastructure for UML models")
        self.assertEqual(journal_paper_two.doi, "10.1016/j.scico.2006.05.011")
        self.assertEqual(journal_paper_two.year, 2007)
        self.assertEqual(journal_paper_two.first_page, 249)
        self.assertEqual(journal_paper_two.last_page, 274)
        self.assertEqual(journal_paper_two.authors, "Leonardo Gresta Paulino Murta;Hamilton Oliveira;Cristine Ribeiro "
                                                    "Dantas;Luiz Gustavo Berno Lopes;Cl\xC3\xA1udia Maria Lima Werner")

        # Journal - Venue
        # one
        self.assertEqual(journal_one.name, "Revista Tecnologia da Informa\xC3\xA7\xC3\xA3o")
        # TODO self.assertEqual(journal_one.qualis,)
        self.assertEqual(journal_one.issn, "1516-9197")
        self.assertEqual(journal_one.jcr, 0)
        # two
        self.assertEqual(journal_two.name, "SCIENCE OF COMPUTER PROGRAMMING")
        # TODO self.assertEqual(journal_one.qualis,)
        self.assertEqual(journal_two.issn, "0167-6423")
        self.assertEqual(journal_two.jcr, 0.775)

    def test3AddConferencePapers(self):
        """Adds the reseacher conference papers and checks if all the information and realtionships with
        venues are correct"""
        add_conference_papers(session=self.session, tree=self.tree, researcher_id=self.researcher_id)
        conferences_papers_database = self.session.query(ConferencePaper).all()
        conference_paper_one, conference_paper_two = conferences_papers_database[0], conferences_papers_database[1]

        conference_one = self.session.query(Conference).filter(Conference.id == conference_paper_one.venue).all()[0]
        conference_two = self.session.query(Conference).filter(Conference.id == conference_paper_two.venue).all()[0]

        # ConferencePapers
        # one
        self.assertEqual(conference_paper_one.researchers[0].id, 1)
        self.assertEqual(conference_paper_one.title, "Charon: Uma M\xC3\xA1quina de Processos Extens\xC3\xADvel "
                                                     "Baseada em Agentes Inteligentes")
        self.assertEqual(conference_paper_one.doi, "DOITESTE")
        self.assertEqual(conference_paper_one.year, 2002)
        self.assertEqual(conference_paper_one.first_page, 236)
        self.assertEqual(conference_paper_one.last_page, 247)
        self.assertEqual(conference_paper_one.authors, "Leonardo Gresta Paulino Murta;M\xC3\xA1rcio de Oliveira "
                                                       "Barros;Cl\xC3\xA1udia Maria Lima Werner")
        # two
        self.assertEqual(conference_paper_two.researchers[0].id, 1)
        self.assertEqual(conference_paper_two.title, "LockED: Uma Abordagem para o Controle de "
                                                     "Altera\xC3\xA7\xC3\xB5es de Artefatos de Software")
        self.assertEqual(conference_paper_two.doi, None)
        self.assertEqual(conference_paper_two.year, 2001)
        self.assertEqual(conference_paper_two.first_page, 348)
        self.assertEqual(conference_paper_two.last_page, 359)
        self.assertEqual(conference_paper_two.authors, "Hugo Vidal Teixeira;Leonardo Gresta Paulino "
                                                       "Murta;Cl\xC3\xA1udia Maria Lima Werner")

        # Venue - Conference
        # one
        self.assertEqual(conference_one.name, "Workshop Iberoamericano de Ingenier\xC3\xADa de Requisitos y Ambientes "
                                              "de Software (IDEAS)")
        # TODO self.assertEqual(conference_one.qualis,)
        # TODO self.assertEqual(conference_one.acronym,)
        self.assertEqual(conference_one.h5, None)

        # two
        self.assertEqual(conference_two.name, "Workshop Iberoamericano de Ingenier\xC3\xADa de Requisitos y Ambientes "
                                              "de Software (IDEAS)")
        # TODO self.assertEqual(conference_two.qualis,)
        # TODO self.assertEqual(conference_two.acronym,)
        self.assertEqual(conference_two.h5, None)

    def test4AddProject(self):
        """Adds all the projects on the .xml file and checks if the information is correct"""
        add_projects(self.session, self.tree)
        projects_database = self.session.query(Project).all()

        project_one, project_two = projects_database[0], projects_database[1]
        # one
        self.assertEqual(project_one.name, "Open Source Software Development Processes in a Commercial Environment - "
                                           "15.000,00 Euros")
        self.assertEqual(project_one.manager, "Guilherme Horta Travassos")
        self.assertEqual(project_one.team, "Leonardo Gresta Paulino Murta;M\xC3\xA1rcio de Oliveira Barros;Cleidson "
                                           "R. B. de Souza;Renata Mendes de Ara\xC3\xBAjo")
        self.assertEqual(project_one.start_year, 2008)
        self.assertEqual(project_one.end_year, 2008)
        # two
        self.assertEqual(project_two.name, "Desafios do Aumento da Maturidade em Organiza\xC3\xA7\xC3\xB5es de "
                                           "Desenvolvimento de Software: Integra\xC3\xA7\xC3\xA3o de "
                                           "Solu\xC3\xA7\xC3\xB5es para Avan\xC3\xA7os em Qualidade de Software - R$ "
                                           "115.835,98")
        self.assertEqual(project_two.manager, "Leonardo Gresta Paulino Murta")
        self.assertEqual(project_two.team, "Ana Regina Cavalcanti da Rocha;Gleison dos Santos Souza;Tayana "
                                           "Conte;Carla Alessandra Lima Reis;Sheila Reinehr;Ricardo de Almeida Falbo")
        self.assertEqual(project_two.start_year, 2008)
        self.assertEqual(project_two.end_year, 2010)

    def test5AddStudents(self):
        """Adds all the students in the .xml and checks if the information is correct without minding the
        relationships """
        add_students(self.session, self.tree, self.researcher_id)
        students_database = self.session.query(Student).all()

        self.assertEqual(students_database[0].name, "Chessman Kennedy Faria Corr\xC3\xAAa")
        self.assertEqual(students_database[1].name, "Heliomar Kann da Rocha Santos")
        self.assertEqual(students_database[2].name, "Alessandreia Marta de Oliveira")
        self.assertEqual(students_database[3].name, "Gleiph Ghiotto Lima de Menezes")
        self.assertEqual(students_database[4].name, "Isabella Almeida da Silva")
        self.assertEqual(students_database[5].name, "Monalessa Perini Barcellos")

    def test6ResearcherStudentRelationship(self):
        """Checks if the relationships between the reseacher and the students are correct"""
        researcher_student_database = self.session.query(ResearcherStudent).all()

        # researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
        # student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
        # type = Column(Enum(Type), primary_key=True)
        # year = Column(Integer)
        # title = Column(String)
        # committee = Column(String)

        # Student 1 - master advisor (CO_ORIENTADOR)
        self.assertEqual(researcher_student_database[0].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[0].student_id, 1)
        self.assertEqual(researcher_student_database[0].type, Type.master_advisor)
        self.assertEqual(researcher_student_database[0].year, 2009)
        self.assertEqual(researcher_student_database[0].title, "Odyssey-MEC: Uma Abordagem para o Controle da "
                                                               "Evolu\xC3\xA7\xC3\xA3o de Modelos Computacionais no "
                                                               "Contexto do Desenvolvimento Dirigido por Modelos")
        self.assertEqual(researcher_student_database[0].committee, None)

        # Student 2 - master advisor (ORIENTADOR_PRINCIPAL)
        self.assertEqual(researcher_student_database[1].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[1].student_id, 2)
        self.assertEqual(researcher_student_database[1].type, Type.master_advisor)
        self.assertEqual(researcher_student_database[1].year, 2011)
        self.assertEqual(researcher_student_database[1].title, "Rumo ao Rejuvenescimento Autom\xC3\xA1tico de Software "
                                                               "Guiado por Atributos de Qualidade")
        self.assertEqual(researcher_student_database[1].committee, None)

        # Student 3 - phd advisor (CO_PRINCIPAL)
        self.assertEqual(researcher_student_database[2].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[2].student_id, 3)
        self.assertEqual(researcher_student_database[2].type, Type.phd_advisor)
        self.assertEqual(researcher_student_database[2].year, 2016)
        self.assertEqual(researcher_student_database[2].title, "Diff Sem\xC3\xA2ntico de Documentos XML")
        self.assertEqual(researcher_student_database[2].committee, None)

        # Student 4 - phd advisor (ORIENTADOR_PRINCIPAL)
        self.assertEqual(researcher_student_database[3].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[3].student_id, 4)
        self.assertEqual(researcher_student_database[3].type, Type.phd_advisor)
        self.assertEqual(researcher_student_database[3].year, 2016)
        self.assertEqual(researcher_student_database[3].title, "On the Nature of Software Merge Conflicts")
        self.assertEqual(researcher_student_database[3].committee, None)

        # Student 5 - master committee
        self.assertEqual(researcher_student_database[4].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[4].student_id, 5)
        self.assertEqual(researcher_student_database[4].type, Type.master_comittee)
        self.assertEqual(researcher_student_database[4].year, 2008)
        self.assertEqual(researcher_student_database[4].title, "Um Mecanismo de Percep\xC3\xA7\xC3\xA3o Baseado em "
                                                               "Modelo para Desenvolvedores de Software")
        self.assertEqual(researcher_student_database[4].committee, "Leonardo Gresta Paulino Murta;Cl\xC3\xA1udia "
                                                                   "Maria Lima Werner;Jano Moreira de Souza;Cleidson "
                                                                   "R. B. de Souza")
        # Student 4 - phd committee
        self.assertEqual(researcher_student_database[5].researcher_id, self.researcher_id)
        self.assertEqual(researcher_student_database[5].student_id, 6)
        self.assertEqual(researcher_student_database[5].type, Type.phd_comittee)
        self.assertEqual(researcher_student_database[5].year, 2009)
        self.assertEqual(researcher_student_database[5].title, "Uma Estrat\xC3\xA9gia para Medi\xC3\xA7\xC3\xA3o de "
                                                               "Software e Avalia\xC3\xA7\xC3\xA3o de Bases de "
                                                               "Medidas para Controle Estat\xC3\xADstico de Processos "
                                                               "de Software em Organiza\xC3\xA7\xC3\xB5es de Alta "
                                                               "Maturidade")
        self.assertEqual(researcher_student_database[5].committee, "Leonardo Gresta Paulino Murta;Ana Regina "
                                                                   "Cavalcanti da Rocha;Gleison dos Santos "
                                                                   "Souza;Ricardo de Almeida Falbo;Geraldo Bonorino "
                                                                   "Xex\xC3\xA9o")

    def test7AddResearcherProject(self):
        """Adds the relationships between the researcher and the projects and check if they are correct"""
        add_researcher_project(self.session)
        reseacher_projects_database = self.session.query(ResearcherProject).all()
        reseacher_project_one, reseacher_project_two = reseacher_projects_database[0], reseacher_projects_database[1]

        # one
        self.assertEqual(reseacher_project_one.project_id, 1)
        self.assertEqual(reseacher_project_one.researcher_id, self.researcher_id)
        self.assertFalse(reseacher_project_one.coordinator)
        # two
        self.assertEqual(reseacher_project_two.project_id, 2)
        self.assertEqual(reseacher_project_two.researcher_id, self.researcher_id)
        self.assertTrue(reseacher_project_two.coordinator)

    def test8AddCoathoursPapers(self):
        """Adds some coathours as researchers and checks if the relationship are correct"""
        # ConferencePaper
        researcher_hugo_vidal = Researcher(name="Hugo Vidal Teixeira")
        self.session.add(researcher_hugo_vidal)
        self.session.flush()
        add_coauthor_papers(self.session)

        conference_paper_database_id = self.session.query(ConferencePaper.id).filter(ConferencePaper.title.contains("LockED")).all()[0]

        self.assertEqual(conference_paper_database_id[0], researcher_hugo_vidal.conference_papers[0].id)

        # JournalPaper
        researcher_hamilton_oliveira = Researcher(name="Hamilton Oliveira")
        self.session.add(researcher_hamilton_oliveira)
        self.session.flush()
        add_coauthor_papers(self.session)

        journal_paper_database_id_one = self.session.query(JournalPaper.id).filter(JournalPaper.title.contains("A Caminho da Manuten")).all()[0][0]
        journal_paper_database_id_two = self.session.query(JournalPaper.id).filter(JournalPaper.title.contains("Odyssey-SCM")).all()[0][0]

        self.assertEqual(journal_paper_database_id_one, researcher_hamilton_oliveira.journal_papers[0].id)
        self.assertEqual(journal_paper_database_id_two, researcher_hamilton_oliveira.journal_papers[1].id)


if __name__ == "__main__":
    unittest.main()
