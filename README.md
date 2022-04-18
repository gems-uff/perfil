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

3. Atualize o arquivo que contém os pesquisadores (e.g., pgc.xlsx) adicionando Nome, ID Lattes e ID Scholar para os que devem ser considerados e indique seu caminho na váriavel "researchers_file" no arquivo [config.py](/config.py). Não se preocupe com as demais colunas, pois elas serão preenchidas automaticamente. 

**CUIDADO** ao colar o ID Lattes. Garanta que o ID do Lattes seja colado como texto, pois caso seja colado como número o Excel irá arredondar o valor e os IDs se tornarão inválidos, ou corresponderão ao ID do Lattes de um pesquisador diferente. 

4. Atualize o horizonte de coleta (variáveis start_year e end_year) e indique o caminho do arquivo que contém os pesquisadores (e.g., pgc.xlsx) em config.py.

5. Indique o valor de similaridade mínima para os nomes de conferências(variável conferences_minimum_similarity), nomes de periódicos(variável journals_minimum_similarity), títulos de publicações em conferências(variável conferences_papers_title_minimum_similarity), títulos de publicações em periódicos(variável journals_papers_title_minimum_similarity) e nomes de projetos(variável project_name_minimum_similarity) em config.py.

6. Use download.py para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

`~/perfil$ python download.py`

7. O programa abrirá uma nova guia com o link de download do currículo lattes no seu navegador principal, confirme o captcha e o download será feito. Após o download ser concluído, mova o .zip baixado para a pasta "lattes".

8. Se ainda houver mais currículos lattes para baixar, o programa irá repetir o passo 7, faça-o até não haver mais arquivos para atualizar.

9. populate_database.py popula o banco de dados, in-memory, usando os lattes dos pesquisadores que estão no arquivo de pesquisadores (passo 3 acima) e gera os arquivos de similares na pasta "output/similarity_xlsx".

`~/perfil$ python populate_database.py`

10. Caso queira, edite os arquivos de [sinônimos](/resources/synonyms) com a saída obtida nos arquivos de similares.

11. Use write_profile.py para que as demais colunas do arquivo que contém os pesquisadores (e.g. pgc.xlsx) sejam populadas usando os dados atuais do Lattes e Google Scholar.

`~/perfil$ python write_profile.py`

12. Caso deseje destacar os resultados de um pesquisador específico, adicione os dados dele no arquivo config.py (variável subject). Os dados desse pesquisador não precisam estar no arquivo que contém os pesquisadores (passo 3 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 3 acima). 

13. Use visualize.py para gerar as boxplots.

`~/perfil$ python visualize.py`

14. Use generate_reseacher_paper_and_title_info.py para gerar arquivos .xlsx de pesquisadores que estão no banco de dados, os que estão no arquivo de pesquisadores, com informações sobre suas publicações, orientações e participações em banca dentro dos anos estabelicidos em config.py. Os arquivos gerados podem ser encontrados na pasta "output/generate_reseacher_paper_and_title_info" com o nome do pesquisador a qual ele pertence.
    1. `~/perfil$ python generate_reseacher_paper_and_title_info.py` exibe uma linha de comando interativa para o usuário escolher **um** pesquisador para gerar o arquivo ou gerar os arquivos para **todos** os pesquisadores.
    2. `~/perfil$ python generate_reseacher_paper_and_title_info.py --all` gera os arquivos de todos os pesquisadores sem precisar de interação com a linha de comando.
    3. `~/perfil$ python generate_reseacher_paper_and_title_info.py --researchers (researcher.id|researcher.lattes_id) +` substitua "(researcher.id|researcher.lattes_id) +" por um ou mais id do banco de dados ou id do lattes dos pesquisadores para gerar apenas os arquivos deles sem precisar de interação com a linha de comando. O id do banco de dados é o mesmo que a ordem no arquivo de pesquisadores.
    4. `~/perfil$ python generate_reseacher_paper_and_title_info.py --ids` mostra no console os ids que os pesquisadores no arquivo de pesquisadores irão ter no banco de dados.


15. Use generate_datacapes.py para gerar relatórios sobre a produção e sumário dos pesquisadores e anual dos pesquisadores [afiliados](/resources/affiliations), esse script também gera o relatório "4n". Deve-se colocar os valores de "normalize_conference_paper" e "normalize_journal_paper", em [config.py](/config.py), como False. Lembrando que a saída é de acordo com o arquivo de pesquisadores. Os arquivos gerados podem ser encontrados na pasta "output/datacapes".

`~/perfil$ python generate_datacapes.py`

## Execução dos testes:

1. Entre no diretório do projeto:

`~$ cd perfil`

2. Ative o ambiente conda que você acabou de criar:

`~/perfil$ pipenv shell`

3. Chame o comando abaixo para executar os testes:

`~/perfil$ python -m unittest database_test.py -v`

## Função dos scripts executáveis:

### database_test.py
Script de teste para verificar se os dados do lattes estão sendo coletados e colocados no banco de dados in-memory.

### download.py
Script para auxiliar o usuário baixar os lattes dos pesquisadores no arquivo de pesquisadores.

### generate_datacapes.py
Script para gerar relatórios de um programa de pós-graduação conforme pedido pela CAPES. Os relatórios são baseados nas publicações em periódicos e conferências e seus respectivos Qualis, usando apenas os pesquisadores afiliados naquele ano.

### generate_reseacher_paper_and_title_info.py
Script com a funcionalidade de gerar arquivos .xlsx com informações, dos pesquisadores no arquivo de pesquisadores, que auxiliam na promoção de títulares.

### populate_database.py
Script que popula o banco de dados in-memory com as informações do lattes dos pesquisadores no arquivo de pesquisadores. Ele também gera os arquivos de nomes similares para conferências, periódicos e projetos.

### visualize.py
Script que gera as boxplots baseado no arquivo de pesquisadores já preenchido pelo script [write_profile.py](write_profile.py)

### write_profile.py
Script com a funcionalidade de preencher as informações dos pesquisadores do arquivo de pesquisadores no mesmo. Usa os dados do Lattes e do Google Scholar.

## Váriaveis do arquivo script.py

* **researchers_file** : váriavel com o caminho do arquivo de pesquisadores.
* **start_year** : ano inicial do horizonte de coleta(inclusive).
* **end_year** : ano final do horizonte de coleta(inclusive).
* **normalize_conference_paper**: Se for atribuído o valor de True, faz com que os artigos de conferência sejam únicos no banco de dados, ou seja, após registrar um dado artigo de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse artigo, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os autores de um dado artigo, que estão no banco de dados, são relacionados com o artigo.
* **normalize_journal_paper**: Se for atribuído o valor de True, faz com que os artigos de periódico sejam únicos no banco de dados, ou seja, após registrar um dado artigo de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse artigo, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os autores de um dado artigo, que estão no banco de dados, são relacionados com o artigo.
* **normalize_project**: Se for atribuído o valor de True, faz com que os projetos sejam únicos no banco de dados, ou seja, após registrar um dado projeto de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse projeto, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os participantes de um dado projeto, que estão no banco de dados, são relacionados com o projeto. 
* **conferences_minimum_similarity** : similaridade mínima entre os nomes de conferência para o software considerar elas as mesmas (valor entre 0 e 1).
* **journals_minimum_similarity** : similaridade mínima entre os nomes de periódicos para o software considerar eles os mesmos (valor entre 0 e 1).
* **conferences_papers_title_minimum_similarity** : similaridade mínima entre os títulos de publicações em conferência para o software considerar eles os mesmos (valor entre 0 e 1).
* **journals_papers_title_minimum_similarity** : similaridade mínima entre os títulos de publicações em periódicos para o software considerar eles os mesmos (valor entre 0 e 1).
* **project_name_minimum_similarity** : similaridade mínima entre os nomes de projetos para o software considerar eles os mesmos (valor entre 0 e 1).
* **subject** : pesquisador a ser destacado quando se gerar as boxplots.
* **qualis_journal_points**: o valor dos pontos de cada nível de Qualis de publicações em periódicos de acordo com a regra para credenciamento como Docente Permanente do PGC
* **qualis_conference_points**: o valor dos pontos de cada nível de Qualis de publicações em conferências de acordo com a regra para credenciamento como Docente Permanente do PGC

## Arquivos

### Sinônimos
Os arquivos de sinônimos se encontram na pasta [/resources/synonyms](/resources/synonyms), sendo eles: conferences_synonyms.xlsx, journals_synonyms.xslx, projects_synonyms.xlsx. Cada linha de cada arquivo representa textos que o software reconhecerá como iguais, sendo que na hora de cadastrar no banco de dados ele usará o nome da primeira coluna.

### Similares
Os arquivos de similares se encontram na pasta "output/similarity_xlsx", sendo eles: conferences_similar.xlsx, journals_similar.xlsx, projects_similar.xlsx. Eles são gerados de acordo com as taxas mínimas no arquivo [config.py](config.py), cada linha contém os nomes que o programa julgou iguais(maior ou igual a taxa mínima) e a primeira coluna é o nome que ele usou ao cadastrar no banco de dados.

### Afiliados
Os arquivos de afiliados se encontran na pasta [/resources/affiliations](/resources/affiliations), sendo eles indicados por seus respectivos anos. Cada arquivo representa os pesquisadores que estavam afiliados naquele ano. Cada pesquisador deve estar em uma linha.

## Logs

### log_file.log
* O arquivo exibe possíveis informações duplicadas nos Lattes, cada linha foi uma tentativa de inserção no banco a qual já havia uma entrada com informações iguais ou parecidas. As informações usadas para esse verificação são separadas por um espaço em branco(" ") seguidas do nome do pesquisador do Lattes que isso ocorreu.
* O arquivo exibe as referências cruzadas ocorridas caso alguma(s) das variáveis normalize_conference_paper, normalize_journal_paper, normalize_project (em [config.py](config.py)) estiver(em) atribuída(s) com True.

A cada execução recomenda-se apagar o arquivo, pois ele é incremental.
