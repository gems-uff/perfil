from config import conferences_synonyms, journals_synonyms
from utils.dict_xlsx_utils import write_dict


def main():
    write_dict(conferences_synonyms)
    write_dict(journals_synonyms)


if __name__ == "__main__":
    main()