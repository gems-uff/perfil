# Perfil

Esse projeto permite a análise do perfil de pesquisadores usando tanto o Lattes quanto o Google Scholar para a coleta de dados e gerando boxplots para a visualização dos resultados.

## Instalação

### Requisitos 
Assumimos que você tem o Python 3.8+ instalado no seu computador.

### Passos para Instalação

1. Clone nosso repositorio:

`~$ git clone https://github.com/gems-uff/perfil.git`

2. Entre no diretório do projeto:

`~$ cd perfil`

3. Instale o pipenv (se ainda não estiver instalado)

`~/perfil$ python -m pip install pipenv`

4. Instale as bibliotecas necessárias:

`~/perfil$ pipenv sync`

## Execução dos scripts:

1. Entre no diretório do projeto:

`~$ cd perfil`

2. Ative o ambiente conda que você acabou de criar:

`~/perfil$ pipenv shell`

3. Atualize o arquivo que contém os pesquisadores (e.g., pgc.xlsx) adicionando Nome, ID Lattes e ID Scholar para os que devem ser considerados. Não se preocupe com as demais colunas, pois elas serão preenchidas automaticamente. 

**CUIDADO** ao colar o ID Lattes. Garanta que o ID do Lattes seja colado como texto, pois caso seja colado como número o Excel irá arredondar o valor e os IDs se tornarão inválidos, ou corresponderão ao ID do Lattes de um pesquisador diferente. 

4. Atualize o horizonte de coleta (variáveis start_year e end_year) e indique o arquivo que contém os pesquisadores (e.g., pgc.xlsx) em config.py. 

5. Use download.py para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

`~/perfil$ python download.py`

6. O programa abrirá uma nova guia com o link de download do currículo lattes no seu navegador principal, confirme o captcha e o download será feito. Após o download ser concluído, mova o .zip baixado para a pasta "lattes".

7. Se ainda houver mais currículos lattes para baixar, o programa irá repetir o passo 6, faça-o até não haver mais arquivos para atualizar.

8. Use populate.py para que as demais colunas do arquivo que contém os pesquisadores (e.g. pgc.xlsx) sejam populadas usando os dados atuais do Lattes e Google Scholar.

`~/perfil$ python populate.py`

9. Caso deseje destacar os resultados de um pesquisador específico, adicione os dados dele no arquivo config.py (variável subject). Os dados desse pesquisador não precisam estar no arquivo que contém os pesquisadores (passo 3 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 3 acima). 

10. Use visualize.py para gerar as boxplots.

`~/perfil$ python visualize.py`
## Execução dos testes:

1. Entre no diretório do projeto:

`~$ cd perfil`

2. Ative o ambiente conda que você acabou de criar:

`~/perfil$ pipenv shell`

3. Chame o comando abaixo para executar os testes:

`~/perfil$ python -m unittest database_test.py -v`
