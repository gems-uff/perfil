import os
import pandas as pd
from utils.dict_xlsx_utils import create_synonyms_dictionary

# The expected input file must have the following columns:
# "ID Lattes" containing the 16-digit number associated with a Lattes CV 
# "ID Scholar" containing the 12-character code associated with a Google Scholar profile
# Extra colums will be ignored.
# The order of the columns does not matter
resources_path = os.getcwd() + os.sep + 'resources' + os.sep
output_path = os.getcwd() + os.sep + 'output' + os.sep
researchers_file = resources_path + 'teste.xlsx'

# The first and last years, inclusive, for collecting metrics.
start_year = 2019
end_year = 2021

# The subject that will be plotted as a red dot in the boxplots.
subject = {
    'Nome': 'Leonardo Gresta Paulino Murta',
    'ID Lattes': '1565296529736448',
    'ID Scholar': 'VEbJeB8AAAAJ'
}

# The file with JCR scores
df = pd.read_excel(resources_path + 'jcr.xlsx')
jcr = dict(zip(df.issn, df.impact))

# The file with conferences' qualis
df_qualis_conferences = pd.read_excel(resources_path+'qualis'+os.sep+'qualis-conferences-2016.xlsx')
conferences_qualis = dict(zip(df_qualis_conferences.title, df_qualis_conferences.qualis))

# The file with journals' qualis
df_qualis_journals = pd.read_excel(resources_path+'qualis'+os.sep+'qualis-journals-2016.xlsx')
journals_qualis = dict(zip(df_qualis_journals.title, df_qualis_journals.qualis))

# Minimum similarities
conferences_minimum_similarity = 0.75
journals_minimum_similarity = 0.75
conferences_papers_title_minimum_similarity = 0.9
journals_papers_title_minimum_similarity = 0.9
project_name_minimum_similarity = 0.6

# The file with conferences' synonyms
conferences_synonyms = create_synonyms_dictionary(resources_path+'synonyms'+os.sep+'conferences_synonyms.xlsx')
journals_synonyms = create_synonyms_dictionary(resources_path+'synonyms'+os.sep+'journals_synonyms.xlsx')
projects_synonyms = create_synonyms_dictionary(resources_path+'synonyms'+os.sep+'projects_synonyms.xlsx')

# The directory that contains the zip files downloaded from the Lattes platform.
lattes_dir = os.getcwd() + os.sep + 'lattes'
if not os.path.exists(lattes_dir):
    os.makedirs(lattes_dir)

# The directory that contains the generated figures.
build_dir = os.getcwd() + os.sep + 'build'
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# The directory that contains the generated figures.
similarity_dir = output_path + 'similarity_xlsx'
if not os.path.exists(similarity_dir):
    os.makedirs(similarity_dir)

# The directory that contains the .xlsx files generated by generate_reseacher_paper_and_title_info.py script.
generate_reseacher_paper_and_title_info_output_dir = output_path + 'generate_reseacher_paper_and_title_info'
if not os.path.exists(generate_reseacher_paper_and_title_info_output_dir):
    os.makedirs(generate_reseacher_paper_and_title_info_output_dir)

generate_datacapes_output_dir = output_path + 'datacapes'
if not os.path.exists(generate_datacapes_output_dir):
    os.makedirs(generate_datacapes_output_dir)
