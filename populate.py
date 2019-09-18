import os
import time
import urllib.request
from datetime import datetime
from zipfile import ZipFile

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree

from config import start_year, end_year, lattes_dir, researchers_file, jcr


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
            profile['Nome'] = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO')[0]
            ano = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO/@ANO-DE-CONCLUSAO')[0]
            if ano != '':
                profile['Ano do Doutorado'] = int(ano)
                profile['Idade Acadêmica'] = datetime.now().year - profile['Ano do Doutorado']
            else:
                profile['Ano do Doutorado'] = '--'
                profile['Idade Acadêmica'] = 0

            profile['Participações em Projetos (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' +
                profile['Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
            profile['Projetos Coordenados (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' +
                profile['Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
            profile['Projetos (total)'] = profile['Participações em Projetos (total)'] + profile[
                'Projetos Coordenados (total)']

            profile['Orientações de Mestrado (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO'))
            profile['Orientações de Doutorado (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO'))
            profile['Orientações (total)'] = profile['Orientações de Mestrado (total)'] + profile[
                'Orientações de Doutorado (total)']

            profile['Bancas de Mestrado (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO'))
            profile['Bancas de Doutorado (total)'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO'))
            profile['Bancas (total)'] = profile['Bancas de Mestrado (total)'] + profile['Bancas de Doutorado (total)']

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

            profile['Participações em Projetos'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(
                    start_year) + ' and @ANO-INICIO<=' + str(
                    end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile[
                    'Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
            profile['Projetos Coordenados'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(
                    start_year) + ' and @ANO-INICIO<=' + str(
                    end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile[
                    'Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
            profile['Projetos'] = profile['Participações em Projetos'] + profile['Projetos Coordenados']

            profile['Orientações de Mestrado'] = len(tree.xpath(
                '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO[@ANO>=' + str(
                    start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Orientações de Doutorado'] = len(tree.xpath(
                '/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO[@ANO>=' + str(
                    start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Orientações'] = profile['Orientações de Mestrado'] + profile['Orientações de Doutorado']

            profile['Bancas de Mestrado'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO[@ANO>=' + str(
                    start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Bancas de Doutorado'] = len(tree.xpath(
                '/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO[@ANO>=' + str(
                    start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Bancas'] = profile['Bancas de Mestrado'] + profile['Bancas de Doutorado']

            profile['Publicações em Congressos'] = len(tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO[@NATUREZA="COMPLETO" and @ANO-DO-TRABALHO>=' + str(
                    start_year) + ' and @ANO-DO-TRABALHO<=' + str(end_year) + ']'))
            profile['Publicações em Periódicos'] = len(tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@NATUREZA="COMPLETO" and @ANO-DO-ARTIGO>=' + str(
                    start_year) + ' and @ANO-DO-ARTIGO<=' + str(end_year) + ']'))
            profile['Publicações'] = profile['Publicações em Congressos'] + profile['Publicações em Periódicos']

            jcr_pub = [e for e in tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO[DADOS-BASICOS-DO-ARTIGO/@NATUREZA="COMPLETO" and DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO>=' + str(
                    start_year) + ' and DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO<=' + str(
                    end_year) + ']/DETALHAMENTO-DO-ARTIGO/@ISSN') if e[:4] + '-' + e[4:] in jcr]
            accepted_jcr_pub = [e for e in tree.xpath(
                '/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-ACEITOS-PARA-PUBLICACAO/ARTIGO-ACEITO-PARA-PUBLICACAO/DETALHAMENTO-DO-ARTIGO/@ISSN')
                                if e[:4] + '-' + e[4:] in jcr]
            profile['Publicações JCR'] = len(jcr_pub)
            profile['Publicações JCR > 1,5'] = len([e for e in jcr_pub if jcr[e[:4] + '-' + e[4:]] > 1.5])
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
        for key, value in profile.items():
            df.at[i, key] = value
        print('\tOk ({:.0f}%).'.format((i+1)/max * 100))
        if not (i+1)%5:
            print('\nPausing for 10 seconds to avoid Google Scholar complaining...\n')
            time.sleep(10)

    print("\nFinished.")

    df.to_excel(researchers_file, index=False)


if __name__ == "__main__":
   main()