import os
import pandas as pd
from utils.dict_xlsx_utils import create_synonyms_dictionary

# The expected input file must have the following columns:
# "ID Lattes" containing the 16-digit number associated with a Lattes CV 
# "ID Scholar" containing the 12-character code associated with a Google Scholar profile
# Extra colums will be ignored.
# The order of the columns does not matter
researchers_file = 'teste.xlsx'

# The first and last years, inclusive, for collecting metrics.
start_year = 2016
end_year = 2020

# The subject that will be plotted as a red dot in the boxplots.
subject = {
    'Nome': 'Leonardo Gresta Paulino Murta',
    'ID Lattes': '1565296529736448',
    'ID Scholar': 'VEbJeB8AAAAJ'
}

# The file with JCR scores
df = pd.read_excel('jcr.xlsx')
jcr = dict(zip(df.issn, df.impact))

# The file with conferences' qualis
df_qualis_conferences = pd.read_excel('qualis-conferences-2016.xlsx')
conferences_qualis = dict(zip(df_qualis_conferences.title, df_qualis_conferences.qualis))

# The file with journals' qualis
df_qualis_journals = pd.read_excel('qualis-journals-2016.xlsx')
journals_qualis = dict(zip(df_qualis_journals.title, df_qualis_journals.qualis))

# Minimum similarities
conferences_minimum_similarity = 0.5
journals_minimum_similarity = 0.5

# The file with conferences' synonyms
conferences_synonyms = create_synonyms_dictionary("conferences_synonyms.xlsx")
journals_synonyms = create_synonyms_dictionary("journals_synonyms.xlsx")

# The directory that contains the zip files downloaded from the Lattes platform.
lattes_dir = os.getcwd() + os.sep + 'lattes'
if not os.path.exists(lattes_dir):
    os.makedirs(lattes_dir)

# The directory that contains the generated figures.
build_dir = os.getcwd() + os.sep + 'build'
if not os.path.exists(build_dir):
    os.makedirs(build_dir)
