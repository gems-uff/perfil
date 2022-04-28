import pandas as pd
import openpyxl


def create_similarity_file(similarity_dict, file_name):
    """Creates the .xlsx similarity file"""
    dict_to_xlsx = dict()
    for key in similarity_dict:
        if similarity_dict[key] not in dict_to_xlsx:
            dict_to_xlsx[similarity_dict[key]] = []
        dict_to_xlsx[similarity_dict[key]].append(key)

    df = pd.DataFrame(dict([(key, pd.Series(value, dtype=pd.StringDtype())) for key, value in dict_to_xlsx.items()])).T
    df.to_excel(file_name + ".xlsx")


def create_synonyms_dictionary(filename):
    """Creates the synonyms dict from the received .xlsx file name"""
    synonyms_dict = dict()
    workbook = openpyxl.load_workbook(filename, read_only=True)
    sheet = workbook.active
    current_value_dict = None
    for row in sheet.rows:
        for cell in row:
            if cell.value is None: break
            elif cell.column == 1: current_value_dict = cell.value
            else: synonyms_dict[cell.value] = current_value_dict

    workbook.close()
    return synonyms_dict