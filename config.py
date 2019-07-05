import os

import pandas as pd

# The expected input file must have the following columns:
# "ID Lattes" containing the 16-digit number associated with a Lattes CV 
# "ID Scholar" containing the 12-character code associated with a Google Scholar profile
# Extra colums will be ignored.
# The order of the columns does not matter
researchers_file = 'pq-1d-5years.xlsx'

# The first and last years, inclusive, for collecting metrics.
start_year = 2014
end_year = 2019

# The subject that will be plotted as a red dot in the boxplots.
subject = {
    'Nome': 'Leonardo Gresta Paulino Murta',
    'ID Lattes': '1565296529736448',
    'ID Scholar': 'VEbJeB8AAAAJ'
}

# The file with JCR scores
df = pd.read_excel('jcr.xlsx')
jcr = dict(zip(df.issn, df.impact))

# The directory that contains the zip files downloaded from the Lattes platform.
lattes_dir = os.getcwd() + os.sep + 'lattes'
if not os.path.exists(lattes_dir):
    os.makedirs(lattes_dir)

# The directory that contains the generated figures.
build_dir = os.getcwd() + os.sep + 'build'
if not os.path.exists(build_dir):
    os.makedirs(build_dir)