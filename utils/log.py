import logging
import inspect


def setup_log_file():
    logging.basicConfig(filename='log_file.log', level=logging.WARNING,
                        format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def log_possible_lattes_duplication(table_name: str, researcher_name: str, *keys):
    '''Adds a new lattes duplication warning to the log file'''

    setup_log_file()

    message = "Function: " + inspect.stack()[1][3] + \
              ". There is a possible duplication in the table " + table_name + " with the following data: "

    for key in keys:
        message += str(key) + " "
    message = message[:-1] + ". Researcher's Lattes: " + researcher_name
    logging.warning(message)


def log_normalize(which_one: str, researcher_id, researcher_name):
    setup_log_file()

    message = "Function: " + inspect.stack()[1][3] + \
              ". The following cross reference was added: " + which_one + ", to this researcher: " + researcher_name + "(id: " + str(researcher_id) + ")"
    logging.warning(message)
