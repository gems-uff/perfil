from database.entities.other_works import ConferenceOrganization, EditorialBoard
import populate_database
import pandas
from config import output_path

# Definir os anos que devem ser analisados
# O intervalo de coleta em "config.py" deve ser maior, pois pode haver participação
# iniciada no passado e ainda não finalizada
START_YEAR = 2021
END_YEAR = 2024

# Words used to identify whether a researcher is char of a conference
CHAIR_WORDS = ['chair', 'coordenador', 'coordenadora', 'coordenação', 'organizador', 'organizadora', 'organização']


def inc(dict, key):
    if key in dict:
        dict[key] += 1
    else:    
        dict[key] = 1


def main():
    session = populate_database.main()
    editorial_boards = session.query(EditorialBoard).all()
    conference_organization = session.query(ConferenceOrganization).all()
    all_metrics = dict()

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Processing {year}...")
        year_metrics = dict()
        for ed in editorial_boards:
            if ed.start_year <= year and (ed.end_year == '' or year <= ed.end_year):
                inc(year_metrics, ed.type.value)
        for co in conference_organization:
            if co.year == year:
                if any(word in co.title.lower() for word in CHAIR_WORDS):
                    inc(year_metrics, "conference_chair")
                else:
                    inc(year_metrics, "conference_committee")

        all_metrics[year] = year_metrics

    pandas.DataFrame.from_dict(all_metrics).to_excel(output_path + "organization.xlsx")
    print("Results saved in 'output/organization.xlsx'")


if __name__ == "__main__":
    main()