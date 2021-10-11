import pandas as pd
import openpyxl


def create_empty_similarity_dict(dictionary):
    """Creates an empty dict with the keys from the dictionary received as an argument, but it values are empty lists"""
    new_dict = dictionary.copy()
    for key in new_dict:
        new_dict[key] = []
    return new_dict


def remove_empty_keys(dictionary):
    """Returns a new dict which is a copy from the dictionary received, but with it's empty lists removed"""
    new_dict = dict()
    for key in dictionary:
        if len(dictionary[key]) > 0: new_dict[key] = dictionary[key]
    return new_dict


def create_similarity_file(similarity_dict, file_name):
    """Creates the .xlsx similarity file"""
    cleaned_dict = remove_empty_keys(similarity_dict)
    df = pd.DataFrame(dict([(key, pd.Series(value, dtype=pd.StringDtype())) for key, value in cleaned_dict.items()])).T
    df.to_excel(file_name + ".xlsx")


def create_synonyms_dictionary(filename):
    """Creates the synonyms dict from the received .xlsx file name"""
    synonyms_dict = dict()
    workbook = openpyxl.load_workbook(filename, read_only=True)
    sheet = workbook.active
    current_key = None
    for row in sheet.rows:
        for cell in row:
            if cell.value is None: break
            elif cell.column == 1:
                current_key = cell.value
                synonyms_dict[current_key] = []
            else: synonyms_dict[current_key].append(cell.value)

    workbook.close()
    return synonyms_dict