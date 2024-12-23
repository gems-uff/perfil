from configured_reports.get_item_info import get_education_attribute_list, get_prize_attribute_list, get_researchers_names, get_last_lattes_update_list, get_phd_college_list, \
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
from configured_reports.user_classes.formacao import Formacao
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
        value_list = get_researchers_names(session, make_cartesian_product_researcher)
    elif item == Pesquisador.ultima_atualizacao_lattes:
        value_list = get_last_lattes_update_list(session, make_cartesian_product_researcher)
    elif item == Pesquisador.doutorado_universidade:
        value_list = get_phd_college_list(session, make_cartesian_product_researcher)
    elif item == Pesquisador.doutorado_ano:
        value_list = get_phd_defense_year_list(session, make_cartesian_product_researcher)
    elif item == Pesquisador.id_google_scholar:
        value_list = get_google_scholar_id_list(session, make_cartesian_product_researcher)
    elif item == Pesquisador.id_lattes:
        value_list = get_lattes_id_list(session, make_cartesian_product_researcher)
    elif item == Conferencia.ano:
        value_list = get_paper_year_list(session, False)
    elif item == Periodico.ano:
        value_list = get_paper_year_list(session, True)
    elif item == Artigo.ano:
        value_list = append_lists(get_paper_year_list(session, False),get_paper_year_list(session, True))
    elif item == Conferencia.titulo_artigo:
        value_list = get_paper_title_list(session, False)
    elif item == Periodico.titulo_artigo:
        value_list = get_paper_title_list(session, True)
    elif item == Artigo.titulo_artigo:
        value_list = append_lists(get_paper_title_list(session, False), get_paper_title_list(session, True))
    elif item == Conferencia.nome:
        value_list = get_venue_names_list(session, False)
    elif item == Periodico.nome:
        value_list = get_venue_names_list(session, True)
    elif item == Artigo.nome:
        value_list = append_lists(get_venue_names_list(session, False), get_venue_names_list(session, True))
    elif item == Conferencia.quantidade_paginas:
        value_list = get_papers_pages_list(session, False)
    elif item == Periodico.quantidade_paginas:
        value_list = get_papers_pages_list(session, True)
    elif item == Artigo.quantidade_paginas:
        value_list = append_lists(get_papers_pages_list(session, False), get_papers_pages_list(session, True))
    elif item == Conferencia.qualis:
        value_list = get_papers_qualis_list(session, False)
    elif item == Periodico.qualis:
        value_list = get_papers_qualis_list(session, True)
    elif item == Artigo.qualis:
        value_list = append_lists(get_papers_qualis_list(session, False), get_papers_qualis_list(session, True))
    elif item == Periodico.jcr:
        value_list = get_jcr_list(session)
    elif item == Conferencia.forum_oficial:
        value_list = get_forum_oficial_list(session, False)
    elif item == Periodico.forum_oficial:
        value_list = get_forum_oficial_list(session, True)
    elif item == Artigo.forum_oficial:
        value_list = append_lists(get_forum_oficial_list(session, False), get_forum_oficial_list(session, True))
    elif item == Conferencia.doi:
        value_list = get_doi_list(session, False)
    elif item == Periodico.doi:
        value_list = get_doi_list(session, True)
    elif item == Artigo.doi:
        value_list = append_lists(get_doi_list(session, False), get_doi_list(session, True))
    elif item == Conferencia.qualis_pontos:
        value_list = get_qualis_points_list(session, False)
    elif item == Periodico.qualis_pontos:
        value_list = get_qualis_points_list(session, True)
    elif item == Artigo.qualis_pontos:
        value_list = append_lists(get_qualis_points_list(session, False), get_qualis_points_list(session, True))
    elif item == Conferencia.autores:
        value_list = get_authors_list(session, False)
    elif item == Periodico.autores:
        value_list = get_authors_list(session, True)
    elif item == Artigo.autores:
        value_list = append_lists(get_authors_list(session, False), get_authors_list(session, True))
    elif item == Periodico.issn:
        value_list = get_issn_list(session)
    elif item == Conferencia.tipo_artigo:
        value_list = get_paper_nature_list(session, False)
    elif item == Periodico.tipo_artigo:
        value_list = get_paper_nature_list(session, True)
    elif item == Artigo.tipo_artigo:
        value_list = append_lists(get_paper_nature_list(session, False), get_paper_nature_list(session, True))
    elif item == Periodico.artigo_aceito:
        value_list = get_journal_accepted_list(session)
    elif item == Conferencia.acronimo:
        value_list = get_conference_acronym_list(session)
    elif item == Orientacao.tipo:
        value_list = get_advisement_type_list(session)
    elif item == Orientacao.estudante:
        value_list = get_advisement_student_list(session)
    elif item == Orientacao.universidade:
        value_list = get_advisement_college_list(session)
    elif item == Orientacao.ano:
        value_list = get_advisement_year_list(session)
    elif item == Orientacao.titulo:
        value_list = get_advisement_title_list(session)
    elif item == Banca.tipo:
        value_list = get_committee_type_list(session)
    elif item == Banca.ano:
        value_list = get_committee_year_list(session)
    elif item == Banca.universidade:
        value_list = get_committee_college_list(session)
    elif item == Banca.aluno_ou_cargo:
        value_list = get_committee_student_list(session)
    elif item == Banca.titulo:
        value_list = get_committee_title_list(session)
    elif item == Banca.membros:
        value_list = get_committee_team(session)
    elif item == Projeto.nome:
        value_list = get_project_name_list(session)
    elif item == Projeto.responsavel:
        value_list = get_project_manager_list(session)
    elif item == Projeto.coordenador:
        value_list = get_project_coordinator_list(session)
    elif item == Projeto.equipe:
        value_list = get_project_team_list(session)
    elif item == Projeto.inicio:
        value_list = get_project_start_year_list(session)
    elif item == Projeto.fim:
        value_list = get_project_end_year_list(session)
    elif item == Patente.nome:
        value_list = get_patent_title_list(session)
    elif item == Patente.tipo:
        value_list = get_patent_type_list(session)
    elif item == Patente.autores:
        value_list = get_patent_authors_list(session)
    elif item == Patente.local:
        value_list = get_patent_local_list(session)
    elif item == Patente.numero:
        value_list = get_patent_number_list(session)
    elif item == Patente.ano:
        value_list = get_patent_year_list(session)
    elif item == Organizacao_Evento.nome:
        value_list = get_conference_management_title_list(session)
    elif item == Organizacao_Evento.ano:
        value_list = get_conference_management_year_list(session)
    elif item == Organizacao_Evento.membros:
        value_list = get_conference_management_committee_list(session)
    elif item == Corpo_Editorial.nome:
        value_list = get_editorial_board_journal_name_list(session)
    elif item == Corpo_Editorial.tipo:
        value_list = get_editorial_board_type_list(session)
    elif item == Corpo_Editorial.inicio:
        value_list = get_editorial_board_start_year_list(session)
    elif item == Corpo_Editorial.fim:
        value_list = get_editorial_board_end_year_list(session)
    elif item == Livro.titulo:
        value_list = get_book_title_list(session, False)
    elif item == Capitulo.titulo:
        value_list = get_book_title_list(session, True)
    elif item == Livro.editora:
        value_list = get_book_publisher_list(session, False)
    elif item == Capitulo.editora:
        value_list = get_book_publisher_list(session, True)
    elif item == Livro.ano:
        value_list = get_book_year_list(session, False)
    elif item == Capitulo.ano:
        value_list = get_book_year_list(session, True)
    elif item == Livro.autores:
        value_list = get_book_authors_list(session, False)
    elif item == Capitulo.autores:
        value_list = get_book_authors_list(session, True)
    elif item == Capitulo.titulo_livro:
        value_list = get_chapter_title_list(session)
    elif item.split('.')[0] == 'Premio':
        value_list = get_prize_attribute_list(session, Premio.mapeamento[item].split('.')[1])
    elif item.split('.')[0] == 'Formacao':
        value_list = get_education_attribute_list(session, Formacao.mapeamento[item].split('.')[1])
    else:
        print("There isn't any information named \"" + item + "\"\n")

    if value_list:
        write_info(worksheet, col, item, value_list)