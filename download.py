import os
import time
import webbrowser

import pandas as pd

from config import researchers_file, lattes_dir


def modification_time(path):
    try:
        timestamp = os.path.getmtime(path)
    except OSError:
        timestamp = -1
    return timestamp


def download(id_lattes):
    path = lattes_dir + os.sep + str(id_lattes) + '.zip'
    url = 'http://buscatextual.cnpq.br/buscatextual/download.do?idcnpq=' + str(id_lattes)

    webbrowser.open(url)

    # waits while the user downloads the file
    timestamp = modification_time(path)
    while timestamp == modification_time(path):
        time.sleep(1)


def main():
    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    max = len(df)
    print('Processing', max, 'researchers...\n')

    for i, row in df.iterrows():
        profile = row.to_dict()
        print(profile['Nome'] + '...')
        if not pd.isnull(profile['ID Lattes']):
            download(profile['ID Lattes'])
        print('\tOk ({:.0f}%).'.format((i + 1) / max * 100))

    print("\nFinished.")


if __name__ == "__main__":
    main()
