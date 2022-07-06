import pandas as pd

import populate_database
from database.database_manager import Researcher
from config import subject, researchers_file, build_dir
from write_profile import generate_researcher_profile_dict
from visualize import boxplot


def main():
    # Comment the line bellow to remove the red dot indicating the performance of the subject in the following boxplot
    # session = populate_database.main(subject)
    # subject.update(generate_researcher_profile_dict(session.query(Researcher).all()[0], session))
    # print('Red dot representing', subject["Nome"])

    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    # Métrica referentes ao horizonte escolhido
    metrics = ['Artigos JCR > 1,5']
    boxplot(df, subject, metrics, 'fig-jcr>1.5.png', vert=False)


if __name__ == "__main__":
   main()
