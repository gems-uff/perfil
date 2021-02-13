import os
import time
import urllib.request
from datetime import datetime
from zipfile import ZipFile

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree

from config import start_year, end_year, lattes_dir, researchers_file, jcr


def calculate_pages(first_page, last_page):
    try:
        return (int(last_page) - int(first_page)) + 1
    except ValueError:
        return 0


def new_article(type, title, forum, year, first_page, last_page):
    return {'Tipo': type, 'Título da Publicação': title, 'Fórum': forum, 'Ano': year,
            'Páginas': calculate_pages(first_page, last_page)}


# get scholar informations which are not about articles
def extract_scholar_information_from_xml(profile, tree):
    new_profile = profile

    new_profile['Nome'] = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO')[0]

    last_lattes_update = tree.xpath('/CURRICULO-VITAE/@DATA-ATUALIZACAO')[0]
    new_profile['Última atualização Lattes'] = last_lattes_update[:2] + '/' + last_lattes_update[
                                                                              2:-4] + '/' + last_lattes_update[
                                                                                            -4:]
    ano = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO/@ANO-DE-CONCLUSAO')[0]
    if ano != '':
        new_profile['Ano do Doutorado'] = int(ano)
        new_profile['Idade Acadêmica'] = datetime.now().year - new_profile['Ano do Doutorado']
    else:
        new_profile['Ano do Doutorado'] = '--'
        new_profile['Idade Acadêmica'] = 0
    new_profile['Participações em Projetos (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' +
        new_profile['Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
    new_profile['Projetos Coordenados (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' +
        new_profile['Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
    new_profile['Projetos (total)'] = new_profile['Participações em Projetos (total)'] + new_profile[
        'Projetos Coordenados (total)']
    new_profile['Orientações de Mestrado (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO'))
    new_profile['Orientações de Doutorado (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO'))
    new_profile['Orientações (total)'] = new_profile['Orientações de Mestrado (total)'] + new_profile[
        'Orientações de Doutorado (total)']
    new_profile['Bancas de Mestrado (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO'))
    new_profile['Bancas de Doutorado (total)'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO'))
    new_profile['Bancas (total)'] = new_profile['Bancas de Mestrado (total)'] + new_profile[
        'Bancas de Doutorado (total)']

    # Information between the years at config.py
    new_profile['Participações em Projetos'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(
            start_year) + ' and @ANO-INICIO<=' + str(
            end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + new_profile[
            'Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
    new_profile['Projetos Coordenados'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(
            start_year) + ' and @ANO-INICIO<=' + str(
            end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + new_profile[
            'Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
    new_profile['Projetos'] = new_profile['Participações em Projetos'] + new_profile['Projetos Coordenados']

    new_profile['Orientações de Mestrado'] = len(tree.xpath(
        '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO[@ANO>=' + str(
            start_year) + ' and @ANO<=' + str(end_year) + ']'))
    new_profile['Orientações de Doutorado'] = len(tree.xpath(
        '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO[@ANO>=' + str(
            start_year) + ' and @ANO<=' + str(end_year) + ']'))
    new_profile['Orientações'] = new_profile['Orientações de Mestrado'] + new_profile['Orientações de Doutorado']

    new_profile['Bancas de Mestrado'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO[@ANO>=' + str(
            start_year) + ' and @ANO<=' + str(end_year) + ']'))
    new_profile['Bancas de Doutorado'] = len(tree.xpath(
        '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO[@ANO>=' + str(
            start_year) + ' and @ANO<=' + str(end_year) + ']'))
    new_profile['Bancas'] = new_profile['Bancas de Mestrado'] + new_profile['Bancas de Doutorado']

    return new_profile


# get informations about a scholar's articles and publications from conferences
def extract_conferences_information_from_xml(profile, tree):
    new_profile = profile

    # only one access to the xml file per attribute

    number_of_conferences = len(tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO'))
    conferences_status = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO/@NATUREZA')  # maybe change the variable name to 'conferences_natures'
    conferences_years = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO/@ANO-DO-TRABALHO')
    conferences_papers_titles = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO/@TITULO-DO-TRABALHO')
    conferences_names = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DETALHAMENTO-DO-TRABALHO/@NOME-DO-EVENTO')
    conferences_papers_first_page = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DETALHAMENTO-DO-TRABALHO/@PAGINA-INICIAL')
    conferences_papers_last_page = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DETALHAMENTO-DO-TRABALHO/@PAGINA-FINAL')

    new_profile['Publicações em Congressos'] = []
    for conferenceIndex in range(number_of_conferences):
        conference_status = conferences_status[conferenceIndex]
        conference_year = int(conferences_years[conferenceIndex])

        if conference_status == "COMPLETO" and start_year <= conference_year <= end_year:
            article = new_article("CONFERENCIA",
                                  conferences_papers_titles[conferenceIndex],
                                  conferences_names[conferenceIndex],
                                  conference_year,
                                  conferences_papers_first_page[conferenceIndex],
                                  conferences_papers_last_page[conferenceIndex])

            new_profile['Publicações em Congressos'].append(article)

    return new_profile


# get information about a scholar's publications from magazines
def extract_publication_information_from_xml(profile, tree):
    new_profile = profile

    # only one access to the xml file per attribute
    number_of_publications = len(tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO'))
    publications_years = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO')
    publications_titles = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO/@TITULO-DO-ARTIGO')
    magazines_names = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DETALHAMENTO-DO-ARTIGO/@TITULO-DO-PERIODICO-OU-REVISTA')
    papers_first_page = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DETALHAMENTO-DO-ARTIGO/@PAGINA-INICIAL')
    papers_last_page = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DETALHAMENTO-DO-ARTIGO/@PAGINA-FINAL')
    magazines_issn = tree.xpath(
        '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DETALHAMENTO-DO-ARTIGO/@ISSN')

    new_profile['Publicações em Periódicos'] = []
    for publicationIndex in range(number_of_publications):
        publication_year = int(publications_years[publicationIndex])

        if start_year <= publication_year <= end_year:
            article = new_article("PERIODICO",
                                  publications_titles[publicationIndex],
                                  magazines_names[publicationIndex],
                                  publication_year,
                                  papers_first_page[publicationIndex], papers_last_page[publicationIndex])
            article['ISSN'] = magazines_issn[publicationIndex][:4] + "-" + magazines_issn[publicationIndex][-4:]
            article['JCR'] = jcr[article['ISSN']] if article['ISSN'] in jcr else 0

            new_profile['Publicações em Periódicos'].append(article)

    return new_profile


def lattes(id):
    """Collects the following metrics from a Lattes CV:
    - Nome
    - Ano Doutorado
    - Idade Acadêmica
    - Participações em Projetos *
    - Projetos Coordenados *
    - Projetos *
    - Orientações de Mestrado *
    - Orientações de Doutorado *
    - Orientações *
    - Bancas de Mestrado *
    - Bancas de Doutorado *
    - Bancas *
    - Publicações em Congressos *
    - Publicações em Periódicos *
    - Publicações *
    - Publicações JCR *
    - Publicações JCR > 1,5 *
    - Aceitações JCR > 1,5
    - Artigos JCR > 1,5
    * Collects the lifetime value appended with '(total)' and the value according to a predefined horizon.\

    Keyword arguments:
    id -- the 16-digit number associated with a Lattes CV
    """
    profile = {}
    with ZipFile(lattes_dir + os.sep + str(id) + '.zip') as zip:
        with zip.open('curriculo.xml') as file:
            tree = etree.parse(file)

            profile = extract_scholar_information_from_xml(profile, tree)
            profile = extract_conferences_information_from_xml(profile, tree)
            profile = extract_publication_information_from_xml(profile, tree)

            profile['Publicações em Congressos (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO[@NATUREZA="COMPLETO"]'))
            profile['Publicações em Periódicos (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@NATUREZA="COMPLETO"]'))
            profile['Publicações (total)'] = profile['Publicações em Congressos (total)'] + profile[
                'Publicações em Periódicos (total)']

            jcr_pub = [e for e in tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO[DADOS-BASICOS-DO-ARTIGO/@NATUREZA="COMPLETO"]/DETALHAMENTO-DO-ARTIGO/@ISSN')
                       if e[:4] + '-' + e[4:] in jcr]
            profile['Publicações JCR (total)'] = len(jcr_pub)
            profile['Publicações JCR > 1,5 (total)'] = len([e for e in jcr_pub if jcr[e[:4] + '-' + e[4:]] > 1.5])

            profile['Quantidade de Publicações em Congressos'] = len(profile['Publicações em Congressos'])
            profile['Quantidade de Publicações em Periódicos'] = len(profile['Publicações em Periódicos'])
            profile['Quantidade de Publicações'] = profile['Quantidade de Publicações em Congressos'] + profile[
                'Quantidade de Publicações em Periódicos']

            accepted_jcr_pub = [e for e in tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-ACEITOS-PARA-PUBLICACAO/ARTIGO-ACEITO-PARA-PUBLICACAO/DETALHAMENTO-DO-ARTIGO/@ISSN')
                                if e[:4] + '-' + e[4:] in jcr]

            profile['Publicações JCR'] = len([e for e in profile['Publicações em Periódicos'] if e['JCR'] > 0])
            profile['Publicações JCR > 1,5'] = len([e for e in profile['Publicações em Periódicos'] if e['JCR'] > 1.5])
            profile['Aceitações JCR > 1,5'] = len([e for e in accepted_jcr_pub if jcr[e[:4] + '-' + e[4:]] > 1.5])
            profile['Artigos JCR > 1,5'] = profile['Publicações JCR > 1,5'] + profile['Aceitações JCR > 1,5']

    return profile


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


def all(id_lattes, id_scholar):
    """Collects all metrics of a given researcher.
    Please cheque the metric list in the documentation of functions lattes, scholar, and normalized.

    Keyword arguments:
    id_lattes -- the 16-digit number associated with a Lattes CV
    id_scholar -- the 12-character code associated with a Google Scholar profile
    """
    profile = lattes(id_lattes)
    profile.update(scholar(id_scholar))
    profile.update(normalized(profile))
    return profile


def main():
    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    max = len(df)
    print('Processing', max, 'researchers...\n')

    for i, row in df.iterrows():
        profile = row.to_dict()
        print(profile['Nome'] + '...')
        if not pd.isnull(profile['ID Lattes']):
            profile.update(lattes(profile['ID Lattes']))
        if not pd.isnull(profile['ID Scholar']):
            profile.update(scholar(profile['ID Scholar']))
        profile.update(normalized(profile))
        # for key, value in profile.items():
        # df.at[i, key] = value  TODO check erro
        print('\tOk ({:.0f}%).'.format((i + 1) / max * 100))
        if not (i + 1) % 5:
            print('\nPausing for 10 seconds to avoid Google Scholar complaining...\n')
            time.sleep(10)

        # print(profile) #testing

    print("\nFinished.")

    df.to_excel(researchers_file, index=False)


if __name__ == "__main__":
    main()
