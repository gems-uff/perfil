"""Analisa dados da Sucupira para identificar produções com colaborações internacionais

É necessário ter arquivos `conferencia_programa {ano}.xls` para os anos analisados no diretório `resources`.
"""
from typing import Optional
import argparse
from collections import defaultdict
import unicodedata
from dataclasses import dataclass, field

from analyze_international_collaborations import read_foreigners

@dataclass
class CoAuthorData():
    source: set[str] = field(default_factory=set)
    title: set[str] = field(default_factory=set)

UNSPECIFIED = "Não Especificado"

def institution_to_str(institution: float|str, country: float|str, concat_country: bool) -> str:
    """Converte institutição que pode ser nan para str"""
    if isinstance(institution, float):
        institution = UNSPECIFIED
    if concat_country and not isinstance(country, float):
        institution = f"{institution}, {country}"
    return institution.strip().title()


def identify_authors_year(
        year: str|int,
        author_dict: Optional[defaultdict[str, CoAuthorData]] = None,
        concat_country: bool = True
    ) -> defaultdict[str, CoAuthorData]:
    """Obtem informações de colaboradores internacionais do arquivo `conferencia_programa {ano}.xls`
    
    Se quiser juntar resultados de diferentes anos, defina `author_dict` externamente
    e passe para serem alterados nesta função. O último resultado terá o valor acumulado.
    """
    if author_dict is None:
        author_dict = defaultdict(CoAuthorData)
    foreigners = read_foreigners(year)

    for i, author in foreigners.iterrows():
        title = institution_to_str(author["Nome IES Titulação"], author["País Titulação"], concat_country)
        source = institution_to_str(author["Instituição de Origem"], author["País da Instituição de Origem"], concat_country)
        author_dict[author["Nome do Participante"].strip().title()].title.add(title)
        author_dict[author["Nome do Participante"].strip().title()].source.add(source)

    return author_dict


def filter_unspecified(institutions: set[str], hide_unspecified: bool) -> set[str]:
    """Remove instituições não espeficicadas"""
    if UNSPECIFIED in institutions and (hide_unspecified or len(institutions) > 1):
        institutions.remove(UNSPECIFIED)
    return institutions

def identify_authors_quarterly(
        start_year: int,
        author_dict: Optional[defaultdict[str, CoAuthorData]] = None,
        concat_country: bool = True
    ) -> defaultdict[str, CoAuthorData]:
    """Analisa colaboradores internacionais do quadriênio"""
    if author_dict is None:
        author_dict = defaultdict(CoAuthorData)

    for year in range(start_year, start_year + 4):
        result = identify_authors_year(year, author_dict, concat_country)
    return result

def main():
    parser = argparse.ArgumentParser(description="Lista colaboradores internacionais")
    parser.add_argument("years", nargs="*", help="Anos escolhidos para lista. Para listar quadriênios, use o prefixo `q` no ano inicial do quadriênio.")
    parser.add_argument("-t", "--title", action="store_true", help="Mostra instuição de titulação ao invés de instituição de origem da publicação. Só é válido quando modo csv não está ativo")
    parser.add_argument("-i", "--no-institution", action="store_true", help="Esconde todas instituições. Só é válido quando modo csv não está ativo.")
    parser.add_argument("-u", "--unspecified", action="store_true", help=f"Exibe '{UNSPECIFIED}' como instituição quando não há informação sobre")
    parser.add_argument("-c", "--csv", action="store_true", help="Exibe como tabela, ao invés de lista")
    parser.add_argument("-s", "--sep", default="\t", help="Separador. Só é válido se o modo csv estiver ativo")
    parser.add_argument("-n", "--no-header", action="store_true", help="Esconder header. Só é válido se o modo csv estiver ativo")
    parser.add_argument("-p", "--no-country",  action="store_true", help="Não adiciona país ao nome da instituição")

    args = parser.parse_args()
    author_dict = defaultdict(CoAuthorData)
    show_institutions = not args.no_institution
    hide_unspecified = not args.unspecified
    concat_country = not args.no_country

    for year in args.years:
        if year.startswith('q'):
            identify_authors_quarterly(int(year[1:]), author_dict, concat_country)
        else:
            identify_authors_year(year, author_dict, concat_country)

    if args.csv:
        if not args.no_header:
            print(args.sep.join(["Colaborador", "Instituição de Origem", "Nome IES Titulação"]))
        for author, coauthor_data in sorted(author_dict.items(), key=lambda x: unicodedata.normalize('NFKD', x[0])):
            source = "; ".join(filter_unspecified(coauthor_data.source, hide_unspecified))
            title = "; ".join(filter_unspecified(coauthor_data.title, hide_unspecified))
            print(args.sep.join([author, source, title]))
    else:
        for author, coauthor_data in sorted(author_dict.items(), key=lambda x: unicodedata.normalize('NFKD', x[0])):
            institutions = filter_unspecified(
                coauthor_data.title if args.title else coauthor_data.source,
                hide_unspecified
            )
            institutions_text = f" ({'; '.join(institutions)})" if show_institutions and institutions else ""
            print(f'- {author}{institutions_text}')
    

if __name__ == '__main__':
    main()