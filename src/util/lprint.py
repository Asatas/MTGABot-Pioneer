import logging


def lprint(text):
    logging.info('%s', text)
    print(text)

def critical_print(text):
    loggerc = logging.getLogger(name='critical')
    loggerc.critical('%s', text)
    print(text)

# use crit except  
def critical_exception(err):
    loggerc = logging.getLogger(name='critical')
    loggerc.exception(err)
