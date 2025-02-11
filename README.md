To read this document in English [click here](/EN-README.md)

# Perfil

Esse projeto permite a análise do perfil de pesquisadores usando tanto o Lattes quanto o Google Scholar para a coleta de dados, depois gerando relatórios e visualizações.

## Documentação

[Trabalho de conclusão de curso sobre a segunda versão](https://github.com/gems-uff/perfil/raw/master/doc/TCC%20Arthur%20Paiva.pdf)

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

5. Ligue ou desligue as variáveis de unificação, para artigos de conferências (unify_conference_paper), artigos de periódicos (unify_journal_paper), projetos (unify_project), livros (unify_book), capítulos de livros (unify_chapter) e patentes (unify_patent). O objetivo dessas variáveis é evitar duplicatas no banco de dados. Por exemplo, quando mais de um autor do artigo está sendo analisado, o programa tenta unificar os artigos e armazena-lo uma única vez no BD. 

6. Indique o valor de similaridade mínima para os nomes de conferências (variável conferences_minimum_similarity), nomes de periódicos (variável journals_minimum_similarity), títulos de publicações em conferências (variável conferences_papers_title_minimum_similarity), títulos de publicações em periódicos (variável journals_papers_title_minimum_similarity) e nomes de projetos (variável project_name_minimum_similarity) em config.py. Autores diferentes do mesmo artigo podem informar nomes diferentes para a conferência, por exemplo, "XXII Simpósio Brasileiro de Engenharia de Software" e "Simpósio Brasileiro de Engenharia de Software (SBES)".

7. Use download.py para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

`~/perfil$ python download.py`

8. O programa abrirá uma nova guia com o link de download do currículo lattes no seu navegador principal, confirme o captcha e o download será feito. Após o download ser concluído, mova o .zip baixado para a pasta [lattes](/lattes) (ou salve-o direto na pasta).

9. Se ainda houver mais currículos lattes para baixar, o programa irá repetir o passo 8, faça-o até não haver mais arquivos para atualizar.

10. populate_database.py popula o banco de dados usando os lattes dos pesquisadores que estão no arquivo de pesquisadores (passo 3 acima) e gera os arquivos de similares na pasta "output/similarity_xlsx".

`~/perfil$ python populate_database.py`

11. Caso queira, edite os arquivos de [sinônimos](/resources/synonyms) com a saída obtida nos arquivos de similares. E caso alguma(s) entrada(s) de um ou mais arquivos de similares esteja(m) errada(s), aumente o(s) valore(s) de similaridade mínima de(as) sua(s) respesctiva(s) variável(is)(passo 6) e refaça os passos 10 e 11.

12. No arquivo de log, "log_file.log", haverá reportes de possíveis duplicações nos currículos Lattes dos pesquisadores, do arquivo de pesquisadores, caso haja alguma. Ele também reporta caso alguma unificação foi feita (elas serão feitas apenas se elas foram ligadas no passo 5). Obs.: Apague o arquivo de log cada vez que executar um script.  

13. Use write_profile.py para que as demais colunas do arquivo que contém os pesquisadores (e.g. pgc.xlsx) sejam populadas usando os dados atuais do Lattes e Google Scholar. O arquivo deve estar fechado.

`~/perfil$ python write_profile.py`

14. Caso deseje destacar os resultados de um pesquisador específico, vá no arquivo [config.py](/config.py), adicione os dados dele na variável "subject" e atribua o valor True para a variável "print_subject". Os dados desse pesquisador não precisam estar no arquivo que contém os pesquisadores (passo 3 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 3 acima).

15. Use visualize.py para gerar as boxplots. E visualize-jcr.1.5.py para gerar boxplots no quesito artigos em periódicos com valor de JCR > 1,5.

`~/perfil$ python visualize.py`

`~/perfil$ python visualize-jcr1.5.py`

16. Use generate_reseacher_progression_report.py para gerar relatórios para ajudar na progressão dos pesquisadores, do arquivo de pesquisadores, usando dados dentro dos anos estabelicidos em [config.py](/config.py). Os arquivos gerados podem ser encontrados na pasta "output/generate_reseacher_progression_report" com o nome do pesquisador a qual ele pertence.
    1. `~/perfil$ python generate_reseacher_progression_report.py` exibe uma linha de comando interativa para o usuário escolher **um** pesquisador para gerar o arquivo ou gerar os arquivos para **todos** os pesquisadores.
    2. `~/perfil$ python generate_reseacher_progression_report.py --all` gera os arquivos de todos os pesquisadores sem precisar de interação com a linha de comando.
    3. `~/perfil$ python generate_reseacher_progression_report.py --researchers (researcher.id|researcher.lattes_id) +` substitua "(researcher.id|researcher.lattes_id) +" por um ou mais id do banco de dados ou id do lattes dos pesquisadores para gerar apenas os arquivos deles sem precisar de interação com a linha de comando. O id do banco de dados é o mesmo que a ordem no arquivo de pesquisadores.
    4. `~/perfil$ python generate_reseacher_progression_report.py --ids` mostra no console os ids que os pesquisadores no arquivo de pesquisadores irão ter no banco de dados.
    
17. Use generate_datacapes.py para gerar relatórios sobre a produção do programa de pós-graduação e de seus docentes [credenciados](/resources/affiliations). Esse script também gera o relatório para ajudar a escolher as "4n" publicações. Deve-se colocar os valores de "normalize_conference_paper" e "normalize_journal_paper", em [config.py](/config.py), como False. Lembrando que a saída é de acordo com o arquivo de pesquisadores. Os arquivos gerados podem ser encontrados na pasta "output/datacapes".

`~/perfil$ python generate_datacapes.py`

18. Use generate_configured_reports.py para gerar relatórios personalizados. Para fazê-lo basta preencher o dicionário "configured_reports" em [config.py](/config.py). Os nomes dos relatórios devem ser as chaves e strings. Os valores das chaves devem ser listas/vetores de atributos das entidades/classes que se quer as informações. Os arquivos gerados podem ser encontrados na pasta "output/configured_reports". 
     * A variável "reports_as_new_worksheets", em [config.py](/config.py), pode ser colocada como True caso queira todos os relátorios como abas de um único arquivo com o nome de "configured_reports.xlsx". 
     * A váriavel "new_worksheet_if_conflict", também em [config.py](/config.py), pode ser colocada como True caso deseje que conflitos no mesmo relátorio sejam escritos em abas diferentes. Conflitos ocorrem quando há mais de uma entidade/classe no mesmo relatório. (Sem ser "Pesquisador". "Pesquisador" **pode** estar acompanhado de mais **uma** outra classe/entidade).
     * As entidades/classes disponíveis para se consultar são: Banca, Capitulo, Conferencia, Corpo_Editorial, Livro, Organizacao_Evento, Orientacao, Patente, Periodico, Pesquisador, Projeto, Artigo. Sendo que Artigo engloba informações em comum sobre Periodico e Conferencia, mas é considerado como outra entidade em caso de conflito. 

`~/perfil$ python generate_configured_reports.py`

19. Use generate_collaboration_graphs.py para visualizar grafos referentes a colaboração entre os pesquisadores dentro do horizonte de coleta. As variáveis "collaboration_graphs_alpha" e "collaboration_graphs_alpha_decay", em [config.py](/config.py), configuram a intensidade da força de expansão do grafo a partir do centro e sua taxa de decaimento até chegar a 0, respectivamente (devem ser entre 0 e 1). Para visualizar a saída acesse http://127.0.0.1:5000/ com o script executando. 

`~/perfil$ python generate_collaboration_graphs.py`

## Execução dos testes:

1. Entre no diretório do projeto:

`~$ cd perfil`

2. Ative o ambiente conda que você acabou de criar:

`~/perfil$ pipenv shell`

3. Chame o comando abaixo para executar os testes:

`~/perfil$ python -m unittest database_test.py -v`

## Função dos scripts executáveis:

### database_test.py
Script de teste para verificar se os dados do lattes estão sendo coletados e inseridos no banco de dados in-memory.

### download.py
Script para auxiliar o usuário baixar os lattes dos pesquisadores no arquivo de pesquisadores.

### generate_collaboration_graphs.py

Script com a funcionalidade de gerar grafos que representam a colaboração na autoria de artigos entre os pesquisadores e sua intensidade durante o período do horizonte de coleta.

### generate_configured_reports.py
Script com a funcionalidade de gerar relátorios personalizados pelo o usuário de acordo com as variáveis configured_reports, reports_as_new_worksheets e new_worksheet_if_conflict usando dados dos currículos Lattes.

### generate_datacapes.py
Script para gerar relatórios de um programa de pós-graduação conforme pedido pela CAPES. Os relatórios são baseados nas publicações em periódicos e conferências e seus respectivos Qualis, usando apenas os pesquisadores credenciados naqueles anos.

### generate_reseacher_progression_report.py
Script com a funcionalidade de gerar relatórios com informações, dos pesquisadores no arquivo de pesquisadores, que auxiliam na progressão dos pesquisadores.

### populate_database.py
Script que popula o banco de dados in-memory com as informações do lattes dos pesquisadores no arquivo de pesquisadores e gera os arquivos de nomes similares para conferências, periódicos e projetos. Também escreve as possíveis duplicações nos currículos Lattes e as unificações feitas no arquivo de log.

### visualize.py
Script que gera as boxplots baseado no arquivo de pesquisadores já preenchido pelo script [write_profile.py](write_profile.py)

### visualize-jcr.1.5.py

Script que gera boxplot de publicações com JCR maior que 1,5 a partir dos dados quantitativos de um arquivo de pesquisadores preenchidos.

### write_profile.py
Script com a funcionalidade de preencher as informações quantitativas dos pesquisadores do arquivo de pesquisadores no mesmo. Usa os dados dos currículos Lattes e do Google Scholar.

## Váriaveis do arquivo config.py

* **resources_path** : Caminho para a pasta de [recursos](/resources).
* **output_path** : Caminho para a pasta das saídas do programa.
* **researchers_file** : váriavel com o caminho do arquivo de pesquisadores.
* **start_year** : ano inicial do horizonte de coleta(inclusive).
* **end_year** : ano final do horizonte de coleta(inclusive).
* **unify_conference_paper**: Se for atribuído o valor de True, faz com que os artigos de conferência sejam únicos no banco de dados, ou seja, após registrar um dado artigo de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse artigo, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os autores de um dado artigo, que estão no banco de dados, são relacionados com o artigo.
* **unify_journal_paper**: Se for atribuído o valor de True, faz com que os artigos de periódico sejam únicos no banco de dados, ou seja, após registrar um dado artigo de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse artigo, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os autores de um dado artigo, que estão no banco de dados, são relacionados com o artigo.
* **unify_project**: Se for atribuído o valor de True, faz com que os projetos sejam únicos no banco de dados, ou seja, após registrar um dado projeto de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse projeto, ele não é registrado de novo. E após registrar todos os pesquisadores, todos os participantes de um dado projeto, que estão no banco de dados, são relacionados com o projeto.
* **unify_book**: Se for atribuído o valor de True, faz com que os livros publicados sejam únicos no banco de dados, ou seja, após registrar um dado livro publicado de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse livro, ele não é registrado de novo.
* **unify_chapter**: Se for atribuído o valor de True, faz com que os capítulos de livros publicados sejam únicos no banco de dados, ou seja, após registrar um dado capítulo de livro publicado de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem esse capítulo, ele não é registrado de novo.
* **unify_patent**: Se for atribuído o valor de True, faz com que patentes sejam únicas no banco de dados, ou seja, após registrar uma dada patente de um Lattes de um pesquisador, se nos Lattes dos pesquisadores seguintes também tiverem essa patente, ela não é registrada de novo.
* **conferences_minimum_similarity** : similaridade mínima entre os nomes de conferência para o software considerar elas as mesmas (valor entre 0 e 1).
* **journals_minimum_similarity** : similaridade mínima entre os nomes de periódicos para o software considerar eles os mesmos (valor entre 0 e 1).
* **conferences_papers_title_minimum_similarity** : similaridade mínima entre os títulos de publicações em conferência para o software considerar eles os mesmos (valor entre 0 e 1).
* **journals_papers_title_minimum_similarity** : similaridade mínima entre os títulos de publicações em periódicos para o software considerar eles os mesmos (valor entre 0 e 1).
* **project_name_minimum_similarity** : similaridade mínima entre os nomes de projetos para o software considerar eles os mesmos (valor entre 0 e 1).
* **datacapes_minimum_similarity_titles**: similaridade mínima entre os títulos de publicações para o software considerar eles os mesmos ao separar os artigos para fazer a produção do programa de pós-graduação no script [generate_datacapes.py](/generate_datacapes.py).
* **subject** : pesquisador a ser destacado quando se gerar as boxplots.
* **print_subject** : Se for atribuído o valor de True, liga a funcionalidade de destacar o pesquisador da variável "subject" quando forem geradas as boxplots.
* **reports_as_new_worksheets** : Se for atribuído o valor de True, ao rodar o script [generate_configured_reports.py](generate_configured_reports.py), ao invés de a saída ser um arquivo para cada relatório, ela será um único arquivo, com o nome de "configured_reports.xlsx", com os relatórios como abas dele.
* **new_worksheet_if_conflict** : Se for atribuído o valor de True, ao rodar o script [generate_configured_reports.py](generate_configured_reports.py), ao acontecer um conflito em um relatório, ou seja, duas entidades/classes (sem ser "Pesquisador") no mesmo relatório, ao invés de reportar erro, o software irá colocar cada entidade conflitante em uma aba do arquivo fazendo produto cartesiano com "Pesquisador" caso o mesmo foi requisitado no relátorio.
* **configured_reports** : Dicionário o qual suas chaves devem ser strings e seus valores listas/vetores com os atributos das classes/entidades os quais o usuário deseja gerar um relatório os contendo.
* **class QualisLevel** : Classe enumeradora com os níveis Qualis que o programa deve considerar.
* **qualis_journal_points**: Dicionário com os valores dos pontos de cada nível de Qualis de publicações em periódicos.
* **qualis_conference_points**: Dicionário com os valores dos pontos de cada nível de Qualis de publicações em conferências.
* **collaboration_graphs_alpha**: O valor da força inicial em que os nós dos grafos do script [generate_collaboration_graphs.py](generate_collaboration_graphs.py) se expandem do centro. Seu valor deve ser entre 0 e 1.
* **collaboration_graphs_alpha_decay**: O valor em que a força inicial dos nós dos grafos do script [generate_collaboration_graphs.py](generate_collaboration_graphs.py) se torna zero, ou seja, a taxa de decaimento até os nós pararem de se mover. Seu valor deve ser entre 0 e 1.
* **df_jcr** : Caminho para o arquivo com os valores de JCR dos periódicos.
* **df_qualis_conferences** : Caminho para o arquivo com os níveis Qualis de conferências.
* **df_qualis_journals** : Caminho para o arquivo com os níveis Qualis de periódicos.
* **conferences_synonyms** : Caminho para o arquivo com os sinônimos de nomes de conferências.
* **journals_synonyms** : Caminho para o arquivo com os sinônimos de nomes de periódicos.
* **projects_synonyms** : Caminho para o arquivo com os sinônimos de nomes de projetos.
* **lattes_dir** : Caminho da pasta que contém os currículos Lattes.
* **affiliations_dir**: Caminho da pasta que contém os arquivos de dos pesquisadores credenciados ao programa de pós-graduação.

## Arquivos

### Sinônimos
Os arquivos de sinônimos se encontram na pasta [/resources/synonyms](/resources/synonyms), sendo eles: conferences_synonyms.xlsx, journals_synonyms.xslx, projects_synonyms.xlsx. Cada linha de cada arquivo representa textos que o software reconhecerá como iguais, sendo que na hora de cadastrar no banco de dados ele usará o nome da primeira coluna. Por exemplo, os textos escritos nas colunas B5, C5, D5 e E5 são todos sinônimos para o listado na coluna A5

### Similares
Os arquivos de similares se encontram na pasta "output/similarity_xlsx", sendo eles: conferences_similar.xlsx, journals_similar.xlsx, projects_similar.xlsx. Eles são gerados de acordo com as taxas mínimas no arquivo [config.py](config.py), cada linha contém os nomes que o programa julgou iguais(maior ou igual a taxa mínima) e a primeira coluna é o nome que ele usou ao cadastrar no banco de dados (mesmo funcionamento que o arquivo de sinônimos). 

### Credenciados
Os arquivos de credenciados ao programa de pós-graduação se encontran na pasta [/resources/affiliations](/resources/affiliations), sendo eles indicados por seus respectivos anos. Cada arquivo representa os pesquisadores que estavam credenciados naquele ano. Cada pesquisador deve estar em uma linha.

## Logs

### log_file.log
* O arquivo exibe possíveis informações duplicadas nos Lattes, cada linha contém informações com os dados para ajudar a identificar a possível duplicação, incluindo o nome da tabela e a função que isso ocorreu. As informações são separadas por um espaço em branco(" ") seguidas do nome do pesquisador do Lattes que isso ocorreu.
* O arquivo exibe as referências cruzadas ocorridas caso alguma(s) das variáveis unify_conference_paper, unify_journal_paper, unify_project, unify_book, unify_chapter, unify_patent (em [config.py](config.py)) estiver(em) atribuída(s) com True.

A cada execução, recomenda-se apagar o arquivo, pois ele é incremental.

## Referências

O código do arquivo [index.html](/collaboration_graphs/templates/index.html) usou como base o código disponível em: https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
