from configured_reports.get_item_info import get_prize_entity_list, get_prize_name_list, get_prize_year_list, get_researchers_names, get_last_lattes_update_list, get_phd_college_list, \
    get_phd_defense_year_list, get_google_scholar_id_list, get_lattes_id_list, get_paper_year_list, \
    get_paper_title_list, get_venue_names_list, get_papers_pages_list, get_papers_qualis_list, get_jcr_list, \
    get_forum_oficial_list, get_doi_list, get_qualis_points_list, get_authors_list, get_issn_list, \
    get_paper_nature_list, get_journal_accepted_list, get_conference_acronym_list, get_advisement_student_list, \
    get_advisement_college_list, get_advisement_year_list, get_advisement_title_list, get_advisement_type_list, \
    get_committee_student_list, get_committee_college_list, get_committee_year_list, get_committee_title_list, \
    get_committee_type_list, get_committee_team, get_project_name_list, get_project_manager_list, \
    get_project_coordinator_list, get_project_team_list, get_project_start_year_list, get_project_end_year_list, \
    get_patent_type_list, get_patent_title_list, get_patent_authors_list, get_patent_local_list, get_patent_number_list, \
    get_patent_year_list, get_conference_management_title_list, get_conference_management_year_list, \
    get_conference_management_committee_list, get_editorial_board_journal_name_list, get_editorial_board_type_list, \
    get_editorial_board_start_year_list, get_editorial_board_end_year_list, get_book_title_list, \
    get_book_publisher_list, get_book_year_list, get_book_authors_list, get_chapter_title_list
from configured_reports.user_classes.banca import Banca
from configured_reports.user_classes.capitulo import Capitulo
from configured_reports.user_classes.conferencia import Conferencia
from configured_reports.user_classes.corpo_editorial import Corpo_Editorial
from configured_reports.user_classes.livro import Livro
from configured_reports.user_classes.organizacao_evento import Organizacao_Evento
from configured_reports.user_classes.orientacao import Orientacao
from configured_reports.user_classes.patente import Patente
from configured_reports.user_classes.periodico import Periodico
from configured_reports.user_classes.pesquisador import Pesquisador
from configured_reports.user_classes.premio import Premio
from configured_reports.user_classes.projeto import Projeto
from configured_reports.user_classes.artigo import Artigo
from configured_reports.util import append_lists


def write_info(worksheet, col, item, list_info):
    """Writes the information list received in the received column. Each list item goes in the row below the previous"""

    row = 1
    worksheet.cell(row=row, column=col, value=item) # Writes the column's header

    for info in list_info:
        row += 1
        worksheet.cell(row=row, column=col, value=info)


def write_item_info(session, item: str, worksheet, col, make_cartesian_product_researcher):
    """Checks which item is received, gets a list containing the information according with the item, then calls the
    function to write it. It also receives information to make the cartesian product with researcher's information or
    not and which other item to make with"""

    if item == Pesquisador.nome:
        researchers_list = get_researchers_names(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, researchers_list)

    elif item == Pesquisador.ultima_atualizacao_lattes:
        last_lattes_update_list = get_last_lattes_update_list(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, last_lattes_update_list)

    elif item == Pesquisador.doutorado_universidade:
        phd_college_list = get_phd_college_list(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, phd_college_list)

    elif item == Pesquisador.doutorado_ano:
        phd_defense_year_list = get_phd_defense_year_list(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, phd_defense_year_list)

    elif item == Pesquisador.id_google_scholar:
        google_scholar_id_list = get_google_scholar_id_list(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, google_scholar_id_list)

    elif item == Pesquisador.id_lattes:
        lattes_id_list = get_lattes_id_list(session, make_cartesian_product_researcher)
        write_info(worksheet, col, item, lattes_id_list)

    elif item == Conferencia.ano:
        conference_papers_year_list = get_paper_year_list(session, False)
        write_info(worksheet, col, item, conference_papers_year_list)

    elif item == Periodico.ano:
        journal_papers_year_list = get_paper_year_list(session, True)
        write_info(worksheet, col, item, journal_papers_year_list)

    elif item == Artigo.ano:
        papers_year_list = append_lists(get_paper_year_list(session, False),get_paper_year_list(session, True))
        write_info(worksheet, col, item, papers_year_list)

    elif item == Conferencia.titulo_artigo:
        conference_paper_title_list = get_paper_title_list(session, False)
        write_info(worksheet, col, item, conference_paper_title_list)

    elif item == Periodico.titulo_artigo:
        journal_paper_title_list = get_paper_title_list(session, True)
        write_info(worksheet, col, item, journal_paper_title_list)

    elif item == Artigo.titulo_artigo:
        paper_title_list = append_lists(get_paper_title_list(session, False), get_paper_title_list(session, True))
        write_info(worksheet, col, item, paper_title_list)

    elif item == Conferencia.nome:
        conference_names_list = get_venue_names_list(session, False)
        write_info(worksheet, col, item, conference_names_list)

    elif item == Periodico.nome:
        journal_names_list = get_venue_names_list(session, True)
        write_info(worksheet, col, item, journal_names_list)

    elif item == Artigo.nome:
        venue_names_list = append_lists(get_venue_names_list(session, False), get_venue_names_list(session, True))
        write_info(worksheet, col, item, venue_names_list)

    elif item == Conferencia.quantidade_paginas:
        conference_papers_pages_list = get_papers_pages_list(session, False)
        write_info(worksheet, col, item, conference_papers_pages_list)

    elif item == Periodico.quantidade_paginas:
        journal_papers_pages_list = get_papers_pages_list(session, True)
        write_info(worksheet, col, item, journal_papers_pages_list)

    elif item == Artigo.quantidade_paginas:
        papers_pages_list = append_lists(get_papers_pages_list(session, False), get_papers_pages_list(session, True))
        write_info(worksheet, col, item, papers_pages_list)

    elif item == Conferencia.qualis:
        conferences_qualis_list = get_papers_qualis_list(session, False)
        write_info(worksheet, col, item, conferences_qualis_list)

    elif item == Periodico.qualis:
        journal_qualis_list = get_papers_qualis_list(session, True)
        write_info(worksheet, col, item, journal_qualis_list)

    elif item == Artigo.qualis:
        papers_qualis_list = append_lists(get_papers_qualis_list(session, False), get_papers_qualis_list(session, True))
        write_info(worksheet, col, item, papers_qualis_list)

    elif item == Periodico.jcr:
        jcr_list = get_jcr_list(session)
        write_info(worksheet, col, item, jcr_list)

    elif item == Conferencia.forum_oficial:
        conference_forum_oficial_list = get_forum_oficial_list(session, False)
        write_info(worksheet, col, item, conference_forum_oficial_list)

    elif item == Periodico.forum_oficial:
        journal_forum_oficial_list = get_forum_oficial_list(session, True)
        write_info(worksheet, col, item, journal_forum_oficial_list)

    elif item == Artigo.forum_oficial:
        forum_oficial_list = append_lists(get_forum_oficial_list(session, False), get_forum_oficial_list(session, True))
        write_info(worksheet, col, item, forum_oficial_list)

    elif item == Conferencia.doi:
        conference_doi_list = get_doi_list(session, False)
        write_info(worksheet, col, item, conference_doi_list)

    elif item == Periodico.doi:
        journal_doi_list = get_doi_list(session, True)
        write_info(worksheet, col, item, journal_doi_list)

    elif item == Artigo.doi:
        doi_list = append_lists(get_doi_list(session, False), get_doi_list(session, True))
        write_info(worksheet, col, item, doi_list)

    elif item == Conferencia.qualis_pontos:
        conference_qualis_points_list = get_qualis_points_list(session, False)
        write_info(worksheet, col, item, conference_qualis_points_list)

    elif item == Periodico.qualis_pontos:
        journal_qualis_points_list = get_qualis_points_list(session, True)
        write_info(worksheet, col, item, journal_qualis_points_list)

    elif item == Artigo.qualis_pontos:
        qualis_points_list = append_lists(get_qualis_points_list(session, False), get_qualis_points_list(session, True))
        write_info(worksheet, col, item, qualis_points_list)

    elif item == Conferencia.autores:
        conference_authors_list = get_authors_list(session, False)
        write_info(worksheet, col, item, conference_authors_list)

    elif item == Periodico.autores:
        journal_authors_list = get_authors_list(session, True)
        write_info(worksheet, col, item, journal_authors_list)

    elif item == Artigo.autores:
        authors_list = append_lists(get_authors_list(session, False), get_authors_list(session, True))
        write_info(worksheet, col, item, authors_list)

    elif item == Periodico.issn:
        issn_list = get_issn_list(session)
        write_info(worksheet, col, item, issn_list)

    elif item == Conferencia.tipo_artigo:
        conference_nature_list = get_paper_nature_list(session, False)
        write_info(worksheet, col, item, conference_nature_list)

    elif item == Periodico.tipo_artigo:
        journal_nature_list = get_paper_nature_list(session, True)
        write_info(worksheet, col, item, journal_nature_list)

    elif item == Artigo.tipo_artigo:
        paper_nature_list = append_lists(get_paper_nature_list(session, False), get_paper_nature_list(session, True))
        write_info(worksheet, col, item, paper_nature_list)

    elif item == Periodico.artigo_aceito:
        journal_papers_accepted_list = get_journal_accepted_list(session)
        write_info(worksheet, col, item, journal_papers_accepted_list)

    elif item == Conferencia.acronimo:
        conference_acronym_list = get_conference_acronym_list(session)
        write_info(worksheet, col, item, conference_acronym_list)

    elif item == Orientacao.tipo:
        advisement_type_list = get_advisement_type_list(session)
        write_info(worksheet, col, item, advisement_type_list)

    elif item == Orientacao.estudante:
        advisement_student_name_list = get_advisement_student_list(session)
        write_info(worksheet, col, item, advisement_student_name_list)

    elif item == Orientacao.universidade:
        advisement_college_list = get_advisement_college_list(session)
        write_info(worksheet, col, item, advisement_college_list)

    elif item == Orientacao.ano:
        advisement_years_list = get_advisement_year_list(session)
        write_info(worksheet, col, item, advisement_years_list)

    elif item == Orientacao.titulo:
        advisement_title_list = get_advisement_title_list(session)
        write_info(worksheet, col, item, advisement_title_list)

    elif item == Banca.tipo:
        committee_type_list = get_committee_type_list(session)
        write_info(worksheet, col, item, committee_type_list)

    elif item == Banca.ano:
        committee_year_list = get_committee_year_list(session)
        write_info(worksheet, col, item, committee_year_list)

    elif item == Banca.universidade:
        committee_college_list = get_committee_college_list(session)
        write_info(worksheet, col, item, committee_college_list)

    elif item == Banca.aluno_ou_cargo:
        committee_student_list = get_committee_student_list(session)
        write_info(worksheet, col, item, committee_student_list)

    elif item == Banca.titulo:
        committee_title_list = get_committee_title_list(session)
        write_info(worksheet, col, item, committee_title_list)

    elif item == Banca.membros:
        committee_team_list = get_committee_team(session)
        write_info(worksheet, col, item, committee_team_list)

    elif item == Projeto.nome:
        projects_name_list = get_project_name_list(session)
        write_info(worksheet, col, item, projects_name_list)

    elif item == Projeto.responsavel:
        project_manager_list = get_project_manager_list(session)
        write_info(worksheet, col, item, project_manager_list)

    elif item == Projeto.coordenador:
        project_coordinator_list = get_project_coordinator_list(session)
        write_info(worksheet, col, item, project_coordinator_list)

    elif item == Projeto.equipe:
        project_team_list = get_project_team_list(session)
        write_info(worksheet, col, item, project_team_list)

    elif item == Projeto.inicio:
        project_start_year_list = get_project_start_year_list(session)
        write_info(worksheet, col, item, project_start_year_list)

    elif item == Projeto.fim:
        project_end_year_list = get_project_end_year_list(session)
        write_info(worksheet, col, item, project_end_year_list)

    elif item == Patente.nome:
        patent_title_list = get_patent_title_list(session)
        write_info(worksheet, col, item, patent_title_list)

    elif item == Patente.tipo:
        patent_type_list = get_patent_type_list(session)
        write_info(worksheet, col, item, patent_type_list)

    elif item == Patente.autores:
        patent_authors_list = get_patent_authors_list(session)
        write_info(worksheet, col, item, patent_authors_list)

    elif item == Patente.local:
        patent_local_list = get_patent_local_list(session)
        write_info(worksheet, col, item, patent_local_list)

    elif item == Patente.numero:
        patent_number_list = get_patent_number_list(session)
        write_info(worksheet, col, item, patent_number_list)

    elif item == Patente.ano:
        patent_year_list = get_patent_year_list(session)
        write_info(worksheet, col, item, patent_year_list)

    elif item == Organizacao_Evento.nome:
        conference_management_title_list = get_conference_management_title_list(session)
        write_info(worksheet, col, item, conference_management_title_list)

    elif item == Organizacao_Evento.ano:
        conference_management_year_list = get_conference_management_year_list(session)
        write_info(worksheet, col, item, conference_management_year_list)

    elif item == Organizacao_Evento.membros:
        conference_management_committee_list = get_conference_management_committee_list(session)
        write_info(worksheet, col, item, conference_management_committee_list)

    elif item == Corpo_Editorial.nome:
        editorial_board_journal_list = get_editorial_board_journal_name_list(session)
        write_info(worksheet, col, item, editorial_board_journal_list)

    elif item == Corpo_Editorial.tipo:
        editorial_board_type_list = get_editorial_board_type_list(session)
        write_info(worksheet, col, item, editorial_board_type_list)

    elif item == Corpo_Editorial.inicio:
        editorial_board_start_list = get_editorial_board_start_year_list(session)
        write_info(worksheet, col, item, editorial_board_start_list)

    elif item == Corpo_Editorial.fim:
        editorial_board_end_list = get_editorial_board_end_year_list(session)
        write_info(worksheet, col, item, editorial_board_end_list)

    elif item == Livro.titulo:
        book_publisher_list = get_book_title_list(session, False)
        write_info(worksheet, col, item, book_publisher_list)

    elif item == Capitulo.titulo:
        chapter_publisher_list = get_book_title_list(session, True)
        write_info(worksheet, col, item, chapter_publisher_list)

    elif item == Livro.editora:
        book_publisher_list = get_book_publisher_list(session, False)
        write_info(worksheet, col, item, book_publisher_list)

    elif item == Capitulo.editora:
        chapter_publisher_list = get_book_publisher_list(session, True)
        write_info(worksheet, col, item, chapter_publisher_list)

    elif item == Livro.ano:
        book_year_list = get_book_year_list(session, False)
        write_info(worksheet, col, item, book_year_list)

    elif item == Capitulo.ano:
        chapter_year_list = get_book_year_list(session, True)
        write_info(worksheet, col, item, chapter_year_list)

    elif item == Livro.autores:
        book_authors_list = get_book_authors_list(session, False)
        write_info(worksheet, col, item, book_authors_list)

    elif item == Capitulo.autores:
        chapter_authors_list = get_book_authors_list(session, True)
        write_info(worksheet, col, item, chapter_authors_list)

    elif item == Capitulo.titulo_livro:
        chapter_title_list = get_chapter_title_list(session)
        write_info(worksheet, col, item, chapter_title_list)

    elif item == Premio.nome:
        prize_name_list = get_prize_name_list(session)
        write_info(worksheet, col, item, prize_name_list)

    elif item == Premio.entidade:
        prize_entity_list = get_prize_entity_list(session)
        write_info(worksheet, col, item, prize_entity_list)

    elif item == Premio.ano:
        prize_year_list = get_prize_year_list(session)
        write_info(worksheet, col, item, prize_year_list)

    else:
        print("There isn't any information named \"" + item + "\"\n")