import os

# The expected input file must have the following columns:
# "ID Lattes" containing the 16-digit number associated with a Lattes CV 
# "ID Scholar" containing the 12-character code associated with a Google Scholar profile
# Extra colums will be ignored.
# The order of the columns does not matter
# The file should use tabs as separator of columns
# The file should use comma as decimal separator

#researchers_file = 'pgc.xlsx'
researchers_file = 'pq-1d.xlsx'
#researchers_file = 'pq-1d-5years.xlsx'

# The first and last years, inclusive, for collecting metrics.

# 10 years horizon
start_year = 2008
end_year = 2018

# 5 years horizon
#start_year = 2013
#end_year = 2018


# The directory that contains the zip files downloaded from the Lattes platform.

lattes_dir = os.getcwd() + os.sep + 'lattes'

# The subject that will be plotted as a red dot in the boxplots.

subject = {
    'Nome': 'Leonardo Gresta Paulino Murta',
    'ID Lattes': '1565296529736448',
    'ID Scholar': 'VEbJeB8AAAAJ'
}