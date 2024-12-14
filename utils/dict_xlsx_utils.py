import pandas as pd
import openpyxl


def write_dict(dict, file_name):
    """Creates the .xlsx file"""
    dict_to_xlsx = dict()
    for key in dict:
        if dict[key] not in dict_to_xlsx:
            dict_to_xlsx[dict[key]] = []
        dict_to_xlsx[dict[key]].append(key)

    df = pd.DataFrame(dict([(key, pd.Series(value, dtype=pd.StringDtype())) for key, value in dict_to_xlsx.items()])).T
    df.to_excel(file_name + ".xlsx")


def read_dict(filename):
    """Creates dictionary from the received .xlsx file name"""
    dict = dict()
    workbook = openpyxl.load_workbook(filename, read_only=True)
    sheet = workbook.active
    first_value = None
    for row in sheet.rows:
        for cell in row:
            if cell.value is None: break
            elif cell.column == 1: first_value = cell.value
            else: dict[cell.value] = first_value

    workbook.close()
    return dict