"""Analisa dados da Sucupira para identificar produções com colaborações internacionais

É necessário ter arquivos `conferencia_programa {ano}.xls` para os anos analisados no diretório `resources`.
"""
import re
from typing import Optional
import warnings
import pandas as pd
import argparse

TResult = tuple[str, float, float, float]


def read_excel(input_path: str, sheet_name: str|int = 0) -> pd.DataFrame:
    """Carrega excel e ignora warnings específicos do openpyxl"""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
        df = pd.read_excel(input_path, engine='openpyxl', sheet_name=sheet_name)
    return df


def identify_year(
        year: str|int,
        products: Optional[set[int]] = None,
        products_with_foreigners: Optional[set[int]] = None
    ) -> TResult:
    """Obtem informações de participante externo e produções do programa do arquivo `conferencia_programa {ano}.xls`
    
    Se quiser juntar resultados de diferentes anos, defina `products` e `products_with_foreigneirs` externamente
    e passe para serem alterados nesta função. O último resultado terá o valor acumulado.
    """
    external = read_excel(f"resources/conferencia_programa {year}.xls", sheet_name="Participante Externo")
    authors = read_excel(f"resources/conferencia_programa {year}.xls", sheet_name="Produções - Autores")
    estrangeiros = set(external[
        (
            (external["Nacionalidade"] == "Estrangeiro") 
            & (external["País da Instituição de Origem"] != "Brasil")
        ) | (
            (external["Nacionalidade"] == "Brasileiro")
            & (~external["País da Instituição de Origem"].isin(["Brasil", ""]))
            & (~external["País da Instituição de Origem"].isna())
        )
         
    ]["Identificador da Pessoa do Participante"])
    bib_products = authors[
        (authors["Tipo de Produção"] == "BIBLIOGRÁFICA")
    ]
    if products is None:
        products = set()
    if products_with_foreigners is None:
        products_with_foreigners = set()
    for i, row in bib_products.iterrows():
        products.add(row["ID da Produção"])
        if row["ID Pessoa do Autor"] in estrangeiros:
            products_with_foreigners.add(row["ID da Produção"])
    return (
        str(year),
        len(products),
        len(products_with_foreigners),
        len(products_with_foreigners)/len(products) * 100
    )


def identify_quarterly(start_year: int, average: bool = True) -> TResult:
    """Analisa quadriênio e calcula média ou valor total"""
    products: set[int] = set()
    products_with_foreigners: set[int] = set()
    for year in range(start_year, start_year + 4):
        result = identify_year(year, products=products, products_with_foreigners=products_with_foreigners)
    if average:
        result = (f'Média {start_year}-{start_year + 3}', result[1] / 4, result[2] / 4, result[3])
    else:
        result = (f'Total {start_year}-{start_year + 3}', result[1], result[2], result[3])
    return result

def main():
    parser = argparse.ArgumentParser(description="Analisa o percentual de colaboração internacional")
    parser.add_argument("years", nargs="*", help="Anos escolhidos para análise. Para analisar quadriênios, use o prefixo `q`, `m` ou `t` no ano inicial do quadriênio. O prefixo `q` olha indidividualmente para os 4 anos do quadriênio. O prefixo `m` calcula a média anual. O prefixo `t` calcula a quantidade total de produções do quadriênio")
    parser.add_argument("-n", "--no-header", action="store_true", help="Esconder header")
    parser.add_argument("-s", "--sep", default="\t", help="Separador")
    
    args = parser.parse_args()
    if not args.no_header:
        print(args.sep.join(["Ano","Total", "Estrangeiros", "Percentual"]))
    for year in args.years:
        if year.startswith('m'):
            print(args.sep.join(map(str, identify_quarterly(int(year[1:]), average=True))))
        elif year.startswith('t'):
            print(args.sep.join(map(str, identify_quarterly(int(year[1:]), average=False))))
        elif year.startswith('q'):
            first_year = int(year[1:])
            for qyear in range(first_year, first_year + 4):
                print(args.sep.join(map(str, identify_year(qyear))))
        else:
            print(args.sep.join(map(str, identify_year(year))))

if __name__ == '__main__':
    main()