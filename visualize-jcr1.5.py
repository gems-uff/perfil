import pandas as pd

import populate_database
from config import subject, researchers_file, build_dir
from visualize import boxplot


def main():
    # Comment the line bellow to remove the red dot indicating the performance of the subject in the following boxplot
    # subject.update(populate.all(subject['ID Lattes'], subject['ID Scholar']))
    # print('Red dot representing', subject["Nome"])

    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    # Métrica referentes ao horizonte escolhido
    metrics = ['Artigos JCR > 1,5']
    boxplot(df, subject, metrics, 'fig-jcr>1.5.png', vert=False)

if __name__ == "__main__":
   main()
