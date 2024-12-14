# Consolidate the synonyms of conferences and journals by merging duplicates

import os
from config import conferences_synonyms, journals_synonyms, resources_path
from utils.dict_xlsx_utils import write_dict


def main():
    write_dict(conferences_synonyms, resources_path + 'synonyms' + os.sep + 'conferences_synonyms')
    write_dict(journals_synonyms, resources_path + 'synonyms' + os.sep + 'journals_synonyms')


if __name__ == "__main__":
    main()