# Perfil

Esse projeto permite a análise do perfil de pesquisadores usando tanto o Lattes quanto o Google Scholar para a coleta de dados e gerando boxplots para a visualização dos resultados.

## Siga os seguintes passos:

1. Atualize o arquivo que contém os pesquisadores (e.g., pgc.tsv) adicionando Nome, ID Lattes e ID Scholar para os que devem ser considerados. Não se preocupe com as demais colunas, pois elas serão preenchidas automaticamente. 

**CUIDADO** ao colar o ID Lattes. Garanta que o ID seja colado como texto, pois caso seja colado como número o Excel vai arredondar o valor e os IDs se tornarão inválidos, ou corresponderão ao ID do Lattes de um pesquisador diferente. 

2. Atualize o horizonte de coleta (variáveis start_year e end_year) e indique o arquivo que contém os pesquisadores (e.g., pgc.tsv) em config.py.

3. Use Download.ipynb para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

4. Use Populate.ipynb para que as demais colunas do arquivo researchers.tsv sejam populadas usando os dados atuais do Lattes e Google Scholar.

5. Caso deseje destacar os resultados de um pesquisador específico, adicione os dados dele no arquivo config.py (variável subject). Os dados desse pesquisador NÃO devem estar no arquivo que contém os pesquisadores (passo 1 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 1 acima). 

6. Use Visualiza.ipynb para gerar as boxplots.

## Observações:

* Para rodar um notebook por completo, selecione Kernel / Restart & Run All.
* Para exportar o arquivo researchers.tsv para o Excel, abra o excel, selecione File / Import e escolha CSV File, use as opções Delimited e encoding UTF-8 e deixe somente Tab marcado como separador.
