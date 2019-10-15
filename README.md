# Perfil

Esse projeto permite a análise do perfil de pesquisadores usando tanto o Lattes quanto o Google Scholar para a coleta de dados e gerando boxplots para a visualização dos resultados.

## Instalação

### Requisitos 
Assumimos que você tem o Python 3.7+ instalado no seu computador.

### Passos para Instalação

1. Clone nosso repositorio:

`~$ git clone https://github.com/gems-uff/perfil.git`

2. Entre no diretório do projeto:

`~$ cd perfil`

3. Instale o pipenv (se ainda não estiver instalado)

`~/perfil$ python3.7 -m pip install pipenv`

4. Instale as bibliotecas necessárias:

`~/perfil$ pipenv install`

## Execução dos scripts:

1. Entre no diretório do projeto:

`~$ cd perfil`

2. Ative o ambiente conda que você acabou de criar:

`~/perfil$ pipenv shell`

3. Atualize o arquivo que contém os pesquisadores (e.g., pgc.xlsx) adicionando Nome, ID Lattes e ID Scholar para os que devem ser considerados. Não se preocupe com as demais colunas, pois elas serão preenchidas automaticamente. 

**CUIDADO** ao colar o ID Lattes. Garanta que o ID do Lattes seja colado como texto, pois caso seja colado como número o Excel irá arredondar o valor e os IDs se tornarão inválidos, ou corresponderão ao ID do Lattes de um pesquisador diferente. 

4. Atualize o horizonte de coleta (variáveis start_year e end_year) e indique o arquivo que contém os pesquisadores (e.g., pgc.xlsx) em config.py. 

5. Use download.py para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

`~/perfil$ python3.7 download.py`

6. Use populate.py para que as demais colunas do arquivo que contém os pesquisadores (e.g. pgc.xlsx) sejam populadas usando os dados atuais do Lattes e Google Scholar.

`~/perfil$ python3.7 populate.py`

7. Caso deseje destacar os resultados de um pesquisador específico, adicione os dados dele no arquivo config.py (variável subject). Os dados desse pesquisador não precisam estar no arquivo que contém os pesquisadores (passo 3 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 3 acima). 

8. Use visualize.py para gerar as boxplots.

`~/perfil$ python3.7 visualize.py`
