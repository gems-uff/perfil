# Perfil

Esse projeto permite a análise do perfil de pesquisadores usando tanto o Lattes quanto o Google Scholar para a coleta de dados e gerando boxplots para a visualização dos resultados.

## Instalação

### Requisitos 
Assumimos que você tem o [Anaconda](https://www.anaconda.com/) instalado no seu computador.

### Passos para Instalação

1. Clone nosso repositorio:
`git clone https://github.com/gems-uff/perfil.git`

2. Entre no diretório do projeto:
`cd perfil`

3 - Crie um ambiente conda:
`conda env create -f environment.yml`

4 - Ative o ambiente conda que você acabou de criar:
`conda activate perfil`

(no Windows esse comando é `source activate perfil`)

## Execução dos scripts:

1. Atualize o arquivo que contém os pesquisadores (e.g., pgc.xlsx) adicionando Nome, ID Lattes e ID Scholar para os que devem ser considerados. Não se preocupe com as demais colunas, pois elas serão preenchidas automaticamente. 

**CUIDADO** ao colar o ID Lattes. Garanta que o ID do Lattes seja colado como texto, pois caso seja colado como número o Excel irá arredondar o valor e os IDs se tornarão inválidos, ou corresponderão ao ID do Lattes de um pesquisador diferente. 

2. Atualize o horizonte de coleta (variáveis start_year e end_year) e indique o arquivo que contém os pesquisadores (e.g., pgc.xlsx) em config.py.

3. Use download.py para baixar os currículos Lattes. Isso pode ser um pouco demorado (30 segundos por CV), mas não precisa ser feito sempre. Faça somente quando houver atualização dos currículos no horizonte de análise.

4. Use populate.py para que as demais colunas do arquivo que contém os pesquisadores (e.g. pgc.xlsx) sejam populadas usando os dados atuais do Lattes e Google Scholar.

5. Caso deseje destacar os resultados de um pesquisador específico, adicione os dados dele no arquivo config.py (variável subject). Os dados desse pesquisador não precisam estar no arquivo que contém os pesquisadores (passo 1 acima). Além disso, o Lattes desse pesquisador deve ser baixado manualmente (o programa só baixa os Lattes dos pesquisadores que estão no arquivo referenciado no passo 1 acima). 

6. Use visualize.py para gerar as boxplots.