import unittest
import os
import config
from lxml import etree
from zipfile import ZipFile
from database.database_manager import start_database
from database.populate.book import *
from database.populate.other_works import *
from database.populate.researcher_and_project import *
from database.populate.titles_support import add_researcher_advisements, add_researcher_committees, \
    ResearcherAdvisement, \
    ResearcherCommittee, AdvisementsTypes, CommitteeTypes
from database.populate.venue_and_paper import add_journal_papers, add_conference_papers, add_coauthor_papers, Journal, \
    Conference, JournalPaper, ConferencePaper, PaperNature
from config import QualisLevel


class DatabaseTestCase(unittest.TestCase):
    session = None
    tree = None
    google_scholar_id = "VEbJeB8AAAAJ"
    researcher_id = 1
    lattes_id = 1565296529736448

    @classmethod
    def setUpClass(cls):
        """Initialize some attributes to make the tests"""
        cls.session = start_database(False)
        with ZipFile("test_resources" + os.sep + "curriculo_test.zip") as zip:
            with zip.open("curriculo_test.xml") as file:
                cls.tree = etree.parse(file)
        # with open("curriculo_test.xml", encoding="ISO-8859-1") as file:
        #     cls.tree = etree.parse(file)

    def test01AddResearcher(self):
        """Adds the researcher which will be used in most of the tests"""
        researcher_id = add_researcher(self.session, self.tree, self.google_scholar_id, self.lattes_id)
        researcher_database = self.session.query(Researcher).filter(Researcher.id == researcher_id).all()[0]

        self.assertEqual(researcher_database.name, "Leonardo Gresta Paulino Murta")
        self.assertEqual(researcher_database.last_lattes_update, "20/01/2021")
        self.assertEqual(researcher_database.phd_college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(researcher_database.phd_defense_year, 2006)
        self.assertEqual(researcher_database.google_scholar_id, self.google_scholar_id)

    def test02AddJournalPapers(self):
        """Adds the reseacher journal papers and checks if all the information and realtionships with
        venues are correct"""
        add_journal_papers(session=self.session, tree=self.tree, researcher_id=self.researcher_id,
                           journals_similarity_dict=dict())
        journals_papers_database = self.session.query(JournalPaper).all()

        journal_paper_one, journal_paper_two = journals_papers_database[0], journals_papers_database[1]
        journal_one = self.session.query(Journal).filter(Journal.id == journal_paper_one.venue).all()[0]
        journal_two = self.session.query(Journal).filter(Journal.id == journal_paper_two.venue).all()[0]

        # JournalPapers
        # one
        self.assertEqual(journal_paper_one.researchers[0].id, 1)
        self.assertEqual(journal_paper_one.title, "A Caminho da Manutenção de Software Baseada em Componentes via "
                                                  "Técnicas de Gerência de Configuração de Software")
        self.assertEqual(journal_paper_one.doi, None)
        self.assertEqual(journal_paper_one.nature, PaperNature.COMPLETE)
        self.assertEqual(journal_paper_one.year, 2005)
        self.assertEqual(journal_paper_one.first_page, 45)
        self.assertEqual(journal_paper_one.last_page, 62)
        self.assertEqual(journal_paper_one.authors, "Leonardo Gresta Paulino Murta;Cristine Ribeiro Dantas;Hamilton "
                                                    "Oliveira;Luiz Gustavo Berno Lopes;Cláudia Maria Lima "
                                                    "Werner")
        # two
        self.assertEqual(journal_paper_two.researchers[0].id, 1)
        self.assertEqual(journal_paper_two.title, "Odyssey-SCM: An Integrated Software Configuration Management "
                                                  "Infrastructure for UML models")
        self.assertEqual(journal_paper_two.nature, PaperNature.COMPLETE)
        self.assertEqual(journal_paper_two.doi, "10.1016/j.scico.2006.05.011")
        self.assertEqual(journal_paper_two.year, 2007)
        self.assertEqual(journal_paper_two.first_page, 249)
        self.assertEqual(journal_paper_two.last_page, 274)
        self.assertEqual(journal_paper_two.authors, "Leonardo Gresta Paulino Murta;Hamilton Oliveira;Cristine Ribeiro "
                                                    "Dantas;Luiz Gustavo Berno Lopes;Cláudia Maria Lima Werner")

        # Journal - Venue
        # one
        self.assertEqual(journal_one.name, "Revista Tecnologia da Informação")
        self.assertEqual(journal_one.qualis,
                         QualisLevel.C)  # with a 0.75 similarity the journal matches with REVISTA TECNOLOGIAS NA EDUCAÇÃO which has a C qualis
        self.assertEqual(journal_one.issn, "1516-9197")
        self.assertEqual(journal_one.jcr, 0)
        # two
        self.assertEqual(journal_two.name, "SCIENCE OF COMPUTER PROGRAMMING (PRINT)")
        self.assertEqual(journal_two.qualis, QualisLevel.A2)
        self.assertEqual(journal_two.issn, "0167-6423")
        self.assertEqual(journal_two.jcr, 0.863)

    def test03AddConferencePapers(self):
        """Adds the reseacher conference papers and checks if all the information and realtionships with
        venues are correct"""
        add_conference_papers(session=self.session, tree=self.tree, researcher_id=self.researcher_id,
                              conferences_similarity_dict=dict())
        conferences_papers_database = self.session.query(ConferencePaper).all()
        conference_paper_one, conference_paper_two = conferences_papers_database[0], conferences_papers_database[1]

        conference_one = self.session.query(Conference).filter(Conference.id == conference_paper_one.venue).all()[0]
        conference_two = self.session.query(Conference).filter(Conference.id == conference_paper_two.venue).all()[0]

        # ConferencePapers
        # one
        self.assertEqual(conference_paper_one.researchers[0].id, 1)
        self.assertEqual(conference_paper_one.title, "Charon: Uma Máquina de Processos Extensível Baseada em Agentes "
                                                     "Inteligentes")
        self.assertEqual(conference_paper_one.doi, "DOITESTE")
        self.assertEqual(conference_paper_one.nature, PaperNature.EXPANDED_ABSTRACT)
        self.assertEqual(conference_paper_one.year, 2002)
        self.assertEqual(conference_paper_one.first_page, 236)
        self.assertEqual(conference_paper_one.last_page, 247)
        self.assertEqual(conference_paper_one.authors, "Leonardo Gresta Paulino Murta;Márcio de Oliveira "
                                                       "Barros;Cláudia Maria Lima Werner")
        # two
        self.assertEqual(conference_paper_two.researchers[0].id, 1)
        self.assertEqual(conference_paper_two.title, "LockED: Uma Abordagem para o Controle de "
                                                     "Alterações de Artefatos de Software")
        self.assertEqual(conference_paper_two.nature, PaperNature.ABSTRACT)
        self.assertEqual(conference_paper_two.doi, None)
        self.assertEqual(conference_paper_two.year, 2001)
        self.assertEqual(conference_paper_two.first_page, 348)
        self.assertEqual(conference_paper_two.last_page, 359)
        self.assertEqual(conference_paper_two.authors, "Hugo Vidal Teixeira;Leonardo Gresta Paulino "
                                                       "Murta;Cláudia Maria Lima Werner")

        # Venue - Conference
        # one
        self.assertEqual(conference_one.name, "Workshop Iberoamericano de Ingeniería de Requisitos y Ambientes de "
                                              "Software (IDEAS)")
        self.assertEqual(conference_one.qualis, None)
        self.assertEqual(conference_one.acronym, "IDEAS")

        # two
        self.assertEqual(conference_two.name,
                         "International Conference on Internet Computing and Internet of Things (ICOMP)")
        self.assertEqual(conference_two.qualis, QualisLevel.B5)
        self.assertEqual(conference_two.acronym, "ICOMP")


    def test04AddProject(self):
        """Adds all the projects on the .xml file and checks if the information is correct"""
        add_projects(self.session, self.tree, self.researcher_id, similarity_dict=dict())
        projects_database = self.session.query(Project).all()

        project_one, project_two = projects_database[0], projects_database[1]
        # one
        self.assertEqual(project_one.name, "Open Source Software Development Processes in a Commercial Environment - "
                                           "15.000,00 Euros")
        self.assertEqual(project_one.manager, "Guilherme Horta Travassos")
        self.assertEqual(project_one.team, "Leonardo Gresta Paulino Murta;Márcio de Oliveira Barros;Cleidson "
                                           "R. B. de Souza;Renata Mendes de Araújo")
        self.assertEqual(project_one.start_year, 2008)
        self.assertEqual(project_one.end_year, 2008)
        # two
        self.assertEqual(project_two.name, "Desafios do Aumento da Maturidade em Organizações de "
                                           "Desenvolvimento de Software: Integração de "
                                           "Soluções para Avanços em Qualidade de Software - R$ "
                                           "115.835,98")
        self.assertEqual(project_two.manager, "Leonardo Gresta Paulino Murta")
        self.assertEqual(project_two.team, "Ana Regina Cavalcanti da Rocha;Gleison dos Santos Souza;Tayana "
                                           "Conte;Carla Alessandra Lima Reis;Sheila Reinehr;Ricardo de Almeida Falbo")
        self.assertEqual(project_two.start_year, 2008)
        self.assertEqual(project_two.end_year, 2010)

    def test05AddResearcherAdvisements(self):
        """Adds all the reseacher advisements from the .xml file and check if all information is correct"""
        add_researcher_advisements(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        # Masters
        masters_advisements = self.session.query(ResearcherAdvisement). \
            filter(ResearcherAdvisement.type == AdvisementsTypes.MASTER).all()
        master_advisement_one, master_advisement_two = masters_advisements[0], masters_advisements[1]

        self.assertEqual(master_advisement_one.researcher_id, 1)
        self.assertEqual(master_advisement_one.student_name, "Chessman Kennedy Faria Corrêa")
        self.assertEqual(master_advisement_one.college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(master_advisement_one.year, 2009)
        self.assertEqual(master_advisement_one.title, "Odyssey-MEC: Uma Abordagem para o Controle da Evolução de "
                                                      "Modelos Computacionais no Contexto do Desenvolvimento Dirigido"
                                                      " por Modelos")

        self.assertEqual(master_advisement_two.researcher_id, 1)
        self.assertEqual(master_advisement_two.student_name, "Heliomar Kann da Rocha Santos")
        self.assertEqual(master_advisement_two.college, "Universidade Federal Fluminense")
        self.assertEqual(master_advisement_two.year, 2011)
        self.assertEqual(master_advisement_two.title, "Rumo ao Rejuvenescimento Automático de Software Guiado por "
                                                      "Atributos de Qualidade")

        # PHD
        phds_advisements = self.session.query(ResearcherAdvisement). \
            filter(ResearcherAdvisement.type == AdvisementsTypes.PHD).all()
        phd_advisement_one, phd_advisement_two = phds_advisements[0], phds_advisements[1]

        self.assertEqual(phd_advisement_one.researcher_id, 1)
        self.assertEqual(phd_advisement_one.student_name, "Alessandreia Marta de Oliveira")
        self.assertEqual(phd_advisement_one.college, "Universidade Federal Fluminense")
        self.assertEqual(phd_advisement_one.year, 2016)
        self.assertEqual(phd_advisement_one.title, "Diff Semântico de Documentos XML")

        self.assertEqual(phd_advisement_two.researcher_id, 1)
        self.assertEqual(phd_advisement_two.student_name, "Gleiph Ghiotto Lima de Menezes")
        self.assertEqual(phd_advisement_two.college, "Universidade Federal Fluminense")
        self.assertEqual(phd_advisement_two.year, 2016)
        self.assertEqual(phd_advisement_two.title, "On the Nature of Software Merge Conflicts")

        # Other Advisements
        bachelor_advisement = self.session.query(ResearcherAdvisement).filter(ResearcherAdvisement.type ==
                                                                              AdvisementsTypes.BACHELOR).all()[0]

        self.assertEqual(bachelor_advisement.researcher_id, 1)
        self.assertEqual(bachelor_advisement.student_name, "Bruno Ferreira Pinto e Fernando Campello")
        self.assertEqual(bachelor_advisement.college, "Universidade Federal Fluminense")
        self.assertEqual(bachelor_advisement.year, 2012)
        self.assertEqual(bachelor_advisement.title, "Diff e Merge de Documentos XML")

        specialization_advisement = self.session.query(ResearcherAdvisement).filter(
            ResearcherAdvisement.type == AdvisementsTypes.SPECIALIZATION).all()[0]

        self.assertEqual(specialization_advisement.researcher_id, 1)
        self.assertEqual(specialization_advisement.student_name, "Jon Karl Weibull")
        self.assertEqual(specialization_advisement.college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(specialization_advisement.year, 2009)
        self.assertEqual(specialization_advisement.title,
                         "Desambiguadores Semânticos Semi-supervisionados: uma análise")

        undergraduate_research_advisement = self.session.query(ResearcherAdvisement).filter(
            ResearcherAdvisement.type == AdvisementsTypes.UNDERGRADUATE_RESEARCH).all()[0]

        self.assertEqual(undergraduate_research_advisement.researcher_id, 1)
        self.assertEqual(undergraduate_research_advisement.student_name, "Clarissa Bruno Tuxen")
        self.assertEqual(undergraduate_research_advisement.college, "Universidade Federal Fluminense")
        self.assertEqual(undergraduate_research_advisement.year, 2015)
        self.assertEqual(undergraduate_research_advisement.title, "Análise de Dados Sócio-Econômicos do Corpo Discente "
                                                                  "da UFF")

    def test06AddResearcherCommittee(self):
        """Adds all the reseacher committee participations from the .xml file and check if all information is correct"""
        add_researcher_committees(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        # BACHELOR
        bachelor_committee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.BACHELOR).all()[0]

        self.assertEqual(bachelor_committee.researcher_id, 1)
        self.assertEqual(bachelor_committee.student_name, "Marcelo Dias Gilano de Mello")
        self.assertEqual(bachelor_committee.college, "Universidade Federal Fluminense")
        self.assertEqual(bachelor_committee.year, 2008)
        self.assertEqual(bachelor_committee.title,
                         "Um Estudo sobre Engenharia de Software para Arquiteturas Orientadas a Serviços")
        self.assertEqual(bachelor_committee.team,
                         "Leonardo Gresta Paulino Murta;Esteban Walter Gonzalez Clua;Teresa Cristina de Aguiar")

        # MASTER
        master_committee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.MASTER).all()[0]

        self.assertEqual(master_committee.researcher_id, 1)
        self.assertEqual(master_committee.student_name, "Isabella Almeida da Silva")
        self.assertEqual(master_committee.college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(master_committee.year, 2008)
        self.assertEqual(master_committee.title, "Um Mecanismo de Percepção Baseado em "
                                                 "Modelo para Desenvolvedores de Software")
        self.assertEqual(master_committee.team, "Leonardo Gresta Paulino Murta;Cláudia "
                                                "Maria Lima Werner;Jano Moreira de Souza;Cleidson "
                                                "R. B. de Souza")
        # MASTER_QUALIFICATION
        master_qualification_committee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.MASTER_QUALIFICATION).all()[0]

        self.assertEqual(master_qualification_committee.researcher_id, 1)
        self.assertEqual(master_qualification_committee.student_name, "Rosane Sfair Huergo")
        self.assertEqual(master_qualification_committee.college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(master_qualification_committee.year, 2013)
        self.assertEqual(master_qualification_committee.title, "A method to identify services using master data, "
                                                               "database reverse engineering and artifact-centric "
                                                               "modeling approach")
        self.assertEqual(master_qualification_committee.team, "Leonardo Gresta Paulino Murta;Paulo de Figueiredo Pires")

        # PHD
        phd_committee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.PHD).all()[0]

        self.assertEqual(phd_committee.researcher_id, 1)
        self.assertEqual(phd_committee.student_name, "Monalessa Perini Barcellos")
        self.assertEqual(phd_committee.college, "Universidade Federal do Rio de Janeiro")
        self.assertEqual(phd_committee.year, 2009)
        self.assertEqual(phd_committee.title, "Uma Estratégia para Medição de Software e Avaliação de Bases de "
                                              "Medidas para Controle Estatístico de Processos de Software em "
                                              "Organizações de Alta Maturidade")
        self.assertEqual(phd_committee.team, "Leonardo Gresta Paulino Murta;Ana Regina "
                                             "Cavalcanti da Rocha;Gleison dos Santos "
                                             "Souza;Ricardo de Almeida Falbo;Geraldo Bonorino "
                                             "Xexéo")

        # PHD_QUALIFICATION
        phd_qualification_committee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.PHD_QUALIFICATION).all()[0]

        self.assertEqual(phd_qualification_committee.researcher_id, 1)
        self.assertEqual(phd_qualification_committee.student_name, "Gustavo Ansaldi Oliva")
        self.assertEqual(phd_qualification_committee.college, "Universidade de São Paulo")
        self.assertEqual(phd_qualification_committee.year, 2014)
        self.assertEqual(phd_qualification_committee.title, "Preprocessing Commits to Improve Change Dependencies "
                                                            "Identification from Version Control Systems: Dealing "
                                                            "with Incomplete and Overloaded Commits")
        self.assertEqual(phd_qualification_committee.team, "Leonardo Gresta Paulino Murta;Christina von Flach Garcia "
                                                           "Chavez;Fábio Kon")

        # SPECIALIZATION
        specialization_commmittee = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.SPECIALIZATION).all()[0]

        self.assertEqual(specialization_commmittee.researcher_id, 1)
        self.assertEqual(specialization_commmittee.student_name, "Edilberto Campos Silva Junior")
        self.assertEqual(specialization_commmittee.college, "Universidade Federal Fluminense")
        self.assertEqual(specialization_commmittee.year, 2003)
        self.assertEqual(specialization_commmittee.title, "Estudo da Avaliação para Sugestão de Procedimentos para "
                                                          "gerenciamento de produtos Perigosos corrosivos")
        self.assertEqual(specialization_commmittee.team, "Gilson Brito Alves Lima;FERNANDO TOLEDO FERRAZ;James "
                                                         "Hall;Osvaldo Luiz Gonçalves Quelhas")

        # CIVIL_SERVICE_EXAMINATION
        civil_service_examination = self.session.query(ResearcherCommittee).filter(
            ResearcherCommittee.type == CommitteeTypes.CIVIL_SERVICE_EXAMINATION).all()[0]

        self.assertEqual(civil_service_examination.researcher_id, 1)
        self.assertTrue(len(civil_service_examination.student_name) > 0)
        self.assertEqual(civil_service_examination.college, "Universidade Federal de Juiz de Fora")
        self.assertEqual(civil_service_examination.year, 2009)
        self.assertEqual(civil_service_examination.title, "Banca de Concurso de Professor Efetivo no nível de "
                                                          "Assistente")
        self.assertEqual(civil_service_examination.team, "Leonardo Gresta Paulino Murta;Regina Maria Maciel "
                                                         "Braga;Aline Pires Vieira de Vasconcelos")

    def test07AddResearcherProject(self):
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

    def test08AddCoathoursPapers(self):
        """Adds some coathours as researchers and checks if the relationship are correct"""
        researcher_hugo_vidal = Researcher(name="Hugo Vidal Teixeira")
        self.session.add(researcher_hugo_vidal)
        self.session.flush()
        add_coauthor_papers(self.session)

        # ConferencePaper
        if config.unify_conference_paper:
            conference_paper_database_id = \
                self.session.query(ConferencePaper.id).filter(ConferencePaper.title.contains("LockED")).all()[0]

            self.assertEqual(conference_paper_database_id[0], researcher_hugo_vidal.conference_papers[0].id)

        # JournalPaper
        researcher_hamilton_oliveira = Researcher(name="Hamilton Oliveira")
        self.session.add(researcher_hamilton_oliveira)
        self.session.flush()
        add_coauthor_papers(self.session)

        if config.unify_journal_paper:
            journal_paper_database_id_one = \
                self.session.query(JournalPaper.id).filter(JournalPaper.title.contains("A Caminho da Manuten")).all()[0][0]
            journal_paper_database_id_two = \
                self.session.query(JournalPaper.id).filter(JournalPaper.title.contains("Odyssey-SCM")).all()[0][0]

            self.assertEqual(journal_paper_database_id_one, researcher_hamilton_oliveira.journal_papers[0].id)
            self.assertEqual(journal_paper_database_id_two, researcher_hamilton_oliveira.journal_papers[1].id)

    def test09AddResearcherConferenceManagement(self):
        """Adds all the conferences managed by the researcher from the .xml file and check if all information is correct"""
        add_researcher_conference_management(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        conferences_managed = self.session.query(ResearcherConferenceManagement).all()
        conference_managed_one, conference_managed_two = conferences_managed[0], conferences_managed[1]

        self.assertEqual(conference_managed_one.researcher_id, 1)
        self.assertEqual(conference_managed_one.title, "Workshop de Manutenção de Software Moderna (WMSWM) ("
                                                       "Coordenador do Comitê de Programa)")
        self.assertEqual(conference_managed_one.year, 2008)
        self.assertEqual(conference_managed_one.committee, "Rosana Teresinha Vaccare Braga;Leonardo Gresta Paulino "
                                                           "Murta")

        self.assertEqual(conference_managed_two.researcher_id, 1)
        self.assertEqual(conference_managed_two.title, "Trilha de Relatos de Experiências do Simpósio Brasileiro de "
                                                       "Qualidade de Software (SBQS) (Coordenador do Comitê de "
                                                       "Programa)")
        self.assertEqual(conference_managed_two.year, 2009)
        self.assertEqual(conference_managed_two.committee, "Leonardo Gresta Paulino Murta")

    def test10AddResearcherEditorialBoard(self):
        """Adds all the reseacher jobs in journals from the .xml file and check if all information is correct"""
        add_researcher_editorial_board(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        editorial_boards_jobs = self.session.query(ResearcherEditorialBoard).all()

        editorial_board_job_one, editorial_board_job_two = editorial_boards_jobs[0], editorial_boards_jobs[1]

        # EDITORIAL_BOARD
        self.assertEqual(editorial_board_job_one.researcher_id, 1)
        self.assertEqual(editorial_board_job_one.journal_name, "Journal of The Brazilian Computer Society (Online)")
        self.assertEqual(editorial_board_job_one.type, EditorialBoardType.EDITORIAL_BOARD)
        self.assertEqual(editorial_board_job_one.start_year, 2013)
        self.assertEqual(editorial_board_job_one.end_year, "")
        # REVISER
        self.assertEqual(editorial_board_job_two.researcher_id, 1)
        self.assertEqual(editorial_board_job_two.journal_name, "Software and Systems Modeling (1619-1366)")
        self.assertEqual(editorial_board_job_two.type, EditorialBoardType.REVISER)
        self.assertEqual(editorial_board_job_two.start_year, 2007)
        self.assertEqual(editorial_board_job_two.end_year, 2007)
        # BACKREF
        researcher = self.session.query(Researcher).filter(Researcher.id == self.researcher_id).all()[0]
        self.assertEqual(editorial_board_job_one, researcher.journal_editorial_boards[0])
        self.assertEqual(editorial_board_job_two, researcher.journal_editorial_boards[1])

    def test11AddResearcherPublishedBooks(self):
        """Adds all the reseacher published books from the .xml file and check if all information is correct"""
        add_researcher_published_books(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        research_published_books = self.session.query(ResearcherPublishedBook).all()[0]

        researcher = self.session.query(Researcher).filter(
            Researcher.id == research_published_books.researcher_id).all()[0]
        book = self.session.query(Book).filter(
            Book.id == research_published_books.published_book_id).all()[0]

        self.assertEqual(researcher.id, self.researcher_id)
        self.assertEqual(book.id, research_published_books.published_book_id)
        self.assertEqual(book.title, "Proceedings of the 30th Brazilian Symposium on Databases")
        self.assertEqual(book.publisher, "Sociedade Brasileira de Computação")
        self.assertEqual(book.year, 2015)
        self.assertEqual(book.authors, "Vanessa Braganholo Murta;Fábio Porto;Eduardo Soares Ogasawara;Javam "
                                       "Machado")

    def test12AddResearchPublishedChapters(self):
        """Adds all the reseacher published chapters in books from the .xml file and check if all information is correct"""
        add_researcher_published_chapters(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        research_published_chapters = self.session.query(ResearcherPublishedBookChapter).all()[0]

        # BACKREF
        researcher = self.session.query(Researcher).filter(
            Researcher.id == research_published_chapters.researcher_id).all()[0]
        chapter = self.session.query(BookChapter).filter(
            BookChapter.id == research_published_chapters.published_book_chapter_id).all()[0]

        self.assertEqual(researcher.id, self.researcher_id)
        self.assertEqual(chapter.id, research_published_chapters.published_book_chapter_id)
        self.assertEqual(chapter.title, "Collaborative Software Engineering")
        self.assertEqual(chapter.publisher, "Springer")
        self.assertEqual(chapter.year, 2010)
        self.assertEqual(chapter.authors, "Leonardo Gresta Paulino Murta;Cláudia Maria Lima Werner;Jacky "
                                          "Estublier")
        self.assertEqual(chapter.chapter_title, "The Configuration Management Role in Collaborative Software "
                                                "Engineering")

    def test13AddResearcherPatentsSoftware(self):
        """Adds all the reseacher patents from the .xml file and check if all information is correct"""
        add_researcher_patents_software(session=self.session, tree=self.tree, researcher_id=self.researcher_id)

        researcher_patents = self.session.query(ResearcherPatent).all()
        software = self.session.query(Patent).filter(Patent.id == researcher_patents[0].patent_id).all()[0]
        patent = self.session.query(Patent).filter(Patent.id == researcher_patents[1].patent_id).all()[0]

        self.assertEqual(researcher_patents[0].researcher_id, 1)
        self.assertEqual(researcher_patents[1].researcher_id, 1)

        # SOFTWARE
        self.assertEqual(software.type, PatentType.SOFTWARE)
        self.assertEqual(software.title, "SAPOS - SISTEMA DE APOIO À PÓS-GRADUAÇÃO")
        self.assertEqual(software.authors, "Bruno de Pinho Schettino;Everton Moreth da Silva;Leonardo Gresta Paulino "
                                           "Murta;Rodrigo Dias Ferreira;Tiago Manuel Padreia Amaro;Vanessa Braganholo"
                                           " Murta")
        self.assertEqual(software.local_of_registry, "INPI - Instituto Nacional da Propriedade Industrial")
        self.assertEqual(software.number, "BR512013001030-6")
        self.assertEqual(software.year, 2013)

        # PATENT
        self.assertEqual(patent.type, PatentType.PATENT)
        self.assertEqual(patent.title, "CONTROLADOR DE CARGA INTELIGENTE")
        self.assertEqual(patent.authors, "Ricardo Carrano;Celio Vinicius Neves de Albuquerque;Debora Christina "
                                         "Muchaluat Saade;Diego Passos;Joacir de Oliveira Silva;Luiz Claudio Schara "
                                         "Magalhães")
        self.assertEqual(patent.local_of_registry, "INPI - Instituto Nacional da Propriedade Industrial")
        self.assertEqual(patent.number, "BR1020180015532")
        self.assertEqual(patent.year, 2018)


if __name__ == "__main__":
    unittest.main()
