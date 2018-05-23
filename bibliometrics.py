from config import start_year, end_year, lattes_dir
import os
from datetime import datetime
from zipfile import ZipFile
from lxml import etree
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
import math
import numpy as np
import requests
import ocr
import calendar
import time
import re

jcr = set(pd.read_csv('jcr.tsv', sep='\t')['ISSN'])

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
    - Publicações Indexadas JCR *
    - Publicações *
    * Collects the lifetime value appended with '(total)' and the value according to a predefined horizon.\

    Keyword arguments:
    id -- the 16-digit number associated with a Lattes CV
    """        
    profile = {}
    with ZipFile(lattes_dir + os.sep + str(id) + '.zip') as zip:
        with zip.open('curriculo.xml') as file:
            tree = etree.parse(file)
            profile['Nome'] = tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO')[0]
            profile['Ano do Doutorado'] = int(tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO/@ANO-DE-CONCLUSAO')[0])
            profile['Idade Acadêmica'] = datetime.now().year - profile['Ano do Doutorado']

            profile['Participações em Projetos (total)'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile['Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
            profile['Projetos Coordenados (total)'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile['Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
            profile['Projetos (total)'] = profile['Participações em Projetos (total)'] + profile['Projetos Coordenados (total)']  
            
            profile['Orientações de Mestrado (total)'] = len(tree.xpath('/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO'))
            profile['Orientações de Doutorado (total)'] = len(tree.xpath('/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO'))
            profile['Orientações (total)'] = profile['Orientações de Mestrado (total)'] + profile['Orientações de Doutorado (total)']  
            
            profile['Bancas de Mestrado (total)'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO'))
            profile['Bancas de Doutorado (total)'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO'))
            profile['Bancas (total)'] = profile['Bancas de Mestrado (total)'] + profile['Bancas de Doutorado (total)']
            
            profile['Publicações em Congressos (total)'] = len(tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO[@NATUREZA="COMPLETO"]'))
            profile['Publicações em Periódicos (total)'] = len(tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@NATUREZA="COMPLETO"]'))
            profile['Publicações Indexadas JCR (total)'] = len([e for e in tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO[DADOS-BASICOS-DO-ARTIGO/@NATUREZA="COMPLETO"]/DETALHAMENTO-DO-ARTIGO/@ISSN') if e[:4] + '-' + e[4:] in jcr])
            profile['Publicações (total)'] = profile['Publicações em Congressos (total)'] + profile['Publicações em Periódicos (total)']

            profile['Participações em Projetos'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(start_year) + ' and @ANO-INICIO<=' + str(end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile['Nome'] + '" and @FLAG-RESPONSAVEL="NAO"]'))
            profile['Projetos Coordenados'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA[@ANO-INICIO>=' + str(start_year) + ' and @ANO-INICIO<=' + str(end_year) + ']/EQUIPE-DO-PROJETO/INTEGRANTES-DO-PROJETO[@NOME-COMPLETO="' + profile['Nome'] + '" and @FLAG-RESPONSAVEL="SIM"]'))
            profile['Projetos'] = profile['Participações em Projetos'] + profile['Projetos Coordenados']  
            
            profile['Orientações de Mestrado'] = len(tree.xpath('/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO[@ANO>=' + str(start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Orientações de Doutorado'] = len(tree.xpath('/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO[@ANO>=' + str(start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Orientações'] = profile['Orientações de Mestrado'] + profile['Orientações de Doutorado']
                    
            profile['Bancas de Mestrado'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-MESTRADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO[@ANO>=' + str(start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Bancas de Doutorado'] = len(tree.xpath('/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO/PARTICIPACAO-EM-BANCA-DE-DOUTORADO/DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO[@ANO>=' + str(start_year) + ' and @ANO<=' + str(end_year) + ']'))
            profile['Bancas'] = profile['Bancas de Mestrado'] + profile['Bancas de Doutorado']
                    
            profile['Publicações em Congressos'] = len(tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS/DADOS-BASICOS-DO-TRABALHO[@NATUREZA="COMPLETO" and @ANO-DO-TRABALHO>=' + str(start_year) + ' and @ANO-DO-TRABALHO<=' + str(end_year) + ']'))
            profile['Publicações em Periódicos'] = len(tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@NATUREZA="COMPLETO" and @ANO-DO-ARTIGO>=' + str(start_year) + ' and @ANO-DO-ARTIGO<=' + str(end_year) + ']'))
            profile['Publicações'] = profile['Publicações em Congressos'] + profile['Publicações em Periódicos']
            profile['Publicações Indexadas JCR'] = len([e for e in tree.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO[DADOS-BASICOS-DO-ARTIGO/@NATUREZA="COMPLETO" and DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO>=' + str(start_year) + ' and DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO<=' + str(end_year) + ']/DETALHAMENTO-DO-ARTIGO/@ISSN') if e[:4] + '-' + e[4:] in jcr])

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
    - Publicações Indexadas JCR
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
    metrics = ['Participações em Projetos', 'Projetos Coordenados', 'Projetos', 'Orientações de Mestrado', 'Orientações de Doutorado', 'Orientações', 'Bancas de Mestrado', 'Bancas de Doutorado', 'Bancas', 'Publicações em Congressos', 'Publicações em Periódicos', 'Publicações Indexadas JCR', 'Publicações', 'Citações', 'H-Index']
    for metric in metrics:
        metric_total = metric + ' (total)'
        if metric_total in profile:
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

def boxplot(df, subject, metrics, legends=None, vert=True, rows=1):
    """metrics should be a 2D matrix"""
    if not legends:
        legends = metrics
        
    plots_last_col = len(metrics) % rows 
    cols = (len(metrics)//rows) + (1 if plots_last_col else 0)
        
    width = 2.5 # boxplot width
    height = 5 # boxplot height
    if not vert:
        width, height = height, width        
    width *= cols # figure width
    height *= rows # figure height

    with plt.xkcd():
        plt.close('all')
        fig = plt.figure(figsize=(width,height))
        for i in range(len(metrics)):
            metric = metrics[i]
            ax = plt.subplot2grid((rows*2,cols), ((i%rows)*2 + (0 if i < len(metrics) - plots_last_col else rows-plots_last_col),i//rows), rowspan=2)
            df.boxplot(column=metric, ax=ax, widths=0.7, vert=vert)

            if vert:
                ax.set_xticklabels([legends[i]])
            else:
                ax.set_yticklabels([legends[i]])

            # data points
            for j, row in df.iterrows():
                x = 1
                y = row[metric]
                if not vert:
                    x, y = y, x
                ax.plot(x, y, 'ko', ms = 4, alpha=0.2, zorder = 3)

            # subject point
            if metric in subject:
                x = 1
                y = subject[metric]
                if not vert:
                    x, y = y, x
                ax.plot(x, y, 'ro', ms = 8, zorder = 4)

    plt.tight_layout()

def download(id):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0', 'Accept-Language': 'en-us,en;q=0.5'}
    url = 'http://buscatextual.cnpq.br/buscatextual/download.do?idcnpq=' + str(id)
    req = session.request('GET', url, headers=headers)
    saved = False
    while not saved:
        html = req.text
        soup = BeautifulSoup(html, "lxml")
        image = soup.find('img', id='image_captcha')
        if image is None: # Without captcha
            cd = req.headers.get('content-disposition')
            filename = re.findall('filename=(\S+);', cd)[0]
            f = open(lattes_dir + os.sep + filename, 'wb')
            f.write(req.content);
            f.close()
            saved = True
        else: # with captcha
            id = soup.find('input', id='idcnpq')['value']
            captchaFilename = '/buscatextual/servlet/captcha?metodo=getImagemCaptcha&noCache=' + str(calendar.timegm(time.gmtime()) * 1000)
            req = session.get('http://buscatextual.cnpq.br' + captchaFilename)
            fcaptcha = open('captcha.png', 'wb')
            fcaptcha.write(req.content);
            fcaptcha.close()
            code = ocr.breakCaptcha('captcha.png')
            os.remove('captcha.png')
            r1 = session.get('http://buscatextual.cnpq.br/buscatextual/servlet/captcha?informado=' + code + '&idcnpq=' + id + '&metodo=validaCaptcha')
            payload = {'metodo': 'captchaValido', 'idcnpq': id, 'idiomaExibicao': '', 'tipo': '', 'informado':''}
            req = session.post('http://buscatextual.cnpq.br/buscatextual/download.do', data=payload, headers=headers);