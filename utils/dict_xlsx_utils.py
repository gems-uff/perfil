import pandas as pd
import openpyxl


def write_dict(dictionary, file_name):
    """Creates the .xlsx file"""
    dict_to_xlsx = dict()
    for key in dictionary:
        value = dictionary[key].upper()
        key = key.upper()
        if key != value:
            if value not in dict_to_xlsx:
                dict_to_xlsx[value] = []
            dict_to_xlsx[value].append(key)

    df = pd.DataFrame(dict([(key, pd.Series(value, dtype=pd.StringDtype())) for key, value in dict_to_xlsx.items()])).T
    df.to_excel(file_name + ".xlsx")


def read_dict(filename):
    """Creates dictionary from the received .xlsx file name"""
    dictionary = dict()
    workbook = openpyxl.load_workbook(filename, read_only=True)
    sheet = workbook.active
    first_value = None
    for row in sheet.rows:
        for cell in row:
            if cell.value is None: break
            elif cell.column == 1: first_value = cell.value.upper()
            else: dictionary[cell.value.upper()] = first_value

    workbook.close()
    return dictionary