# Perfil-PGC

Esse programa permite a análise da produção científica de pesquisadores usando tanto o Lattes quanto o Google Scholar.

Primeiro, atualize o arquivo professores.csv adicionando Nome, ID Lattes e ID Scholar para os professores que devem ser considerados. Não se preocupe com as demais colunas. Elas serão preenchidas automaticamente. Também atualize o horizonte de coleta em bibliometrics.py, alterando os valores das variáveis _start_year e _end_year.

Posteriormente, use Download.ipynb para baixar os currículos Lattes. Isso pode ser um pouco demorado (20 segundos por CV), mas não precisa ser feito sempre.

Depois, use Populate.ipynb para que as demais colunas do arquivo professores.csv sejam populadas usando os dados atuais do Lattes e Google Scholar.

Finalmente, use Visualiza.ipynb para gerar as boxplots.

Observações:

* Para exportar o arquivo professores.csv para o Excel, abra o excel, selecione File / Import e escolha CSV File, use as opções Delimited e encoding UTF-8 e deixe somente Tab marcado como separador.