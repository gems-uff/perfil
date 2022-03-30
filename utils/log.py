import logging
import inspect


def log_primary_key_error(what: str, *keys):
    '''Adds a new primary key warning to the log file'''

    logging.basicConfig(filename='primary_key_warnings.log', level=logging.WARNING,
                        format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    message = "Function: " + inspect.stack()[1][3] + \
              ". It wasn't possible to insert this " + what + " with the following primary key: "

    for key in keys:
        message += str(key) + " "
    message = message[:-1]
    logging.warning(message)
