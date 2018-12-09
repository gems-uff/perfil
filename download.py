import calendar
import os
import re
import time
from zipfile import ZipFile

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree

import ocr
from config import lattes_dir, researchers_file


def download(id_lattes):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}
    url = 'http://buscatextual.cnpq.br/buscatextual/download.do?idcnpq=' + str(id_lattes)
    req = session.request('GET', url, headers=headers)
    saved = False
    while not saved:
        html = req.text
        soup = BeautifulSoup(html, "lxml")
        image = soup.find('img', id='image_captcha')
        try: # sometimes we receive an error page
            if image is None:  # Without captcha
                cd = req.headers.get('content-disposition')
                filename = re.findall('filename=(\S+);', cd)[0]
                with open(lattes_dir + os.sep + filename, 'wb') as file:
                    file.write(req.content)
                with ZipFile(lattes_dir + os.sep + filename) as zip: # just to check if it is actually a Lattes CV
                    with zip.open('curriculo.xml') as file:
                        etree.parse(file).xpath('/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO')[0]
                saved = True
            else:  # with captcha
                id_lattes = soup.find('input', id='idcnpq')['value']
                captchaFilename = '/buscatextual/servlet/captcha?metodo=getImagemCaptcha&noCache=' + str(calendar.timegm(time.gmtime()) * 1000)
                req = session.get('http://buscatextual.cnpq.br' + captchaFilename)
                with open('captcha.png', 'wb') as file:
                    file.write(req.content)
                code = ocr.breakCaptcha('captcha.png')
                os.remove('captcha.png')
                session.get('http://buscatextual.cnpq.br/buscatextual/servlet/captcha?informado=' + code + '&idcnpq=' + id_lattes + '&metodo=validaCaptcha')
                payload = {'metodo': 'captchaValido', 'idcnpq': id_lattes, 'idiomaExibicao': '', 'tipo': '', 'informado': ''}
                req = session.post('http://buscatextual.cnpq.br/buscatextual/download.do', data=payload, headers=headers);
        except:
            print('\tRetrying... ')
            session = requests.Session()
            url = 'http://buscatextual.cnpq.br/buscatextual/download.do?idcnpq=' + str(id_lattes)
            req = session.request('GET', url, headers=headers)


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