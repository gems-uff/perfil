import os
import enum
import pandas as pd
from utils.dict_xlsx_utils import create_synonyms_dictionary
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
from configured_reports.user_classes.projeto import Projeto
from configured_reports.user_classes.artigo import Artigo

# The expected input file must have the following columns:
# "ID Lattes" containing the 16-digit number associated with a Lattes CV 
# "ID Scholar" containing the 12-character code associated with a Google Scholar profile
# Extra colums will be ignored.
# The order of the columns does not matter
resources_path = os.getcwd() + os.sep + 'resources' + os.sep
output_path = os.getcwd() + os.sep + 'output' + os.sep
researchers_file = resources_path + 'pgc.xlsx'

# The first and last years, inclusive, for collecting metrics.
start_year = 2021
end_year = 2023


# Tries to make each input on the database unique
unify_conference_paper = False
unify_journal_paper = False
unify_project = False
unify_book = False
unify_chapter = False
unify_patent = False

# Minimum similarities
conferences_minimum_similarity = 0.75
journals_minimum_similarity = 0.75
conferences_papers_title_minimum_similarity = 0.9
journals_papers_title_minimum_similarity = 0.9
project_name_minimum_similarity = 0.9
datacapes_minimum_similarity_titles = 0.75

# The subject that will be plotted as a red dot in the boxplots.
subject = {
    'Nome': 'Leonardo Gresta Paulino Murta',
    'ID Lattes': '1565296529736448',
    'ID Scholar': 'VEbJeB8AAAAJ'
}

print_subject = False

# Reports configured by the user
reports_as_new_worksheets = False
new_worksheet_if_conflict = False

configured_reports = {
    "journalsJCR": [
        Pesquisador.nome,
        Periodico.titulo_artigo,
        Periodico.ano,
        Periodico.nome,
        Periodico.forum_oficial,
        Periodico.issn,
        Periodico.jcr
    ],
}

class QualisLevel(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    C = "C"
    NC = "NC"

# Dictionary to get the qualis level enum by the qualis string
qualis_switch = {
    "A1": QualisLevel.A1,
    "A2": QualisLevel.A2,
    "A3": QualisLevel.A3,
    "A4": QualisLevel.A4,
    "B1": QualisLevel.B1,
    "B2": QualisLevel.B2,
    "B3": QualisLevel.B3,
    "B4": QualisLevel.B4,
    "C": QualisLevel.C,
    "NC": QualisLevel.NC
}

# Dictionaries to get the sim-cred points by qualis and venue
qualis_journal_points = {
    QualisLevel.A1: 1.0,
    QualisLevel.A2: 0.875,
    QualisLevel.A3: 0.75,
    QualisLevel.A4: 0.625,
    QualisLevel.B1: 0.5,
    QualisLevel.B2: 0.2,
    QualisLevel.B3: 0.1,
    QualisLevel.B4: 0.05,
    QualisLevel.C: 0.0,
    QualisLevel.NC: 0.0
}

qualis_conference_points = {
    QualisLevel.A1: 1.0,
    QualisLevel.A2: 0.875,
    QualisLevel.A3: 0.75,
    QualisLevel.A4: 0.625,
    QualisLevel.B1: 0.5,
    QualisLevel.B2: 0.2,
    QualisLevel.B3: 0.1,
    QualisLevel.B4: 0.05,
    QualisLevel.C: 0.0,
    QualisLevel.NC: 0.0
}

# The speed at which the nodes expand further from the center of the graph
collaboration_graphs_alpha = 0.3
# The rate at which the nodes speed approaches 0
collaboration_graphs_alpha_decay = 0.2

# The file with JCR scores
df_jcr = pd.read_excel(resources_path + 'jcr' + os.sep + 'jcr-2022.xlsx')
jcr = dict(zip(df_jcr.issn, df_jcr.if_2022))

# The file with conferences' qualis
df_qualis_conferences = pd.read_excel(resources_path + 'qualis' + os.sep + 'qualis-conferences-2020.xlsx')
conferences_qualis = dict((f'{titulo} ({sigla})', estrato) for (sigla, titulo, estrato) in zip(df_qualis_conferences.sigla, df_qualis_conferences.titulo, df_qualis_conferences.estrato))

# The file with journals' qualis
df_qualis_journals = pd.read_excel(resources_path + 'qualis' + os.sep + 'qualis-journals-2020.xlsx')
journals_qualis = dict(zip(df_qualis_journals.titulo, df_qualis_journals.estrato))

# The file with conferences' synonyms
conferences_synonyms = create_synonyms_dictionary(resources_path + 'synonyms' + os.sep + 'conferences_synonyms.xlsx')
journals_synonyms = create_synonyms_dictionary(resources_path + 'synonyms' + os.sep + 'journals_synonyms.xlsx')
projects_synonyms = create_synonyms_dictionary(resources_path + 'synonyms' + os.sep + 'projects_synonyms.xlsx')

# The directory that contains the zip files downloaded from the Lattes platform.
lattes_dir = resources_path + 'lattes'
if not os.path.exists(lattes_dir):
    os.makedirs(lattes_dir)

# The directory that contains the generated figures.
build_dir = output_path + 'build'
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# The directory that contains the affiliation files
affiliations_dir = resources_path + 'affiliations'
if not os.path.exists(affiliations_dir):
    os.makedirs(affiliations_dir)

# The directory that contains the similarity files.
similarity_dir = output_path + 'similarity_xlsx'
if not os.path.exists(similarity_dir):
    os.makedirs(similarity_dir)

# The directory that contains the .xlsx files generated by generate_reseacher_progression_report.py script.
generate_reseacher_progression_report_output_dir = output_path + 'generate_reseacher_progression_report'
if not os.path.exists(generate_reseacher_progression_report_output_dir):
    os.makedirs(generate_reseacher_progression_report_output_dir)

generate_datacapes_output_dir = output_path + 'datacapes'
if not os.path.exists(generate_datacapes_output_dir):
    os.makedirs(generate_datacapes_output_dir)

generate_reports_output_dir = output_path + 'configured_reports'
if not os.path.exists(generate_reports_output_dir):
    os.makedirs(generate_reports_output_dir)
