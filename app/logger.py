import logging 
from logging import Logger

def get_logger(name: str, filepath: str):
    """Get our logger object to use for messages.

    Inputs:
        name (str): The name of the logging object.
        file_path (str): File path to create a file (Do not create the file if it already exists) and record messages in it. 

    Returns:
        The requested logging object.
    """
    # https://www.programcreek.com/python/example/10123/logging.getLoggerClass Example 3
    # https://www.programcreek.com/python/?code=TD22057%2Finsteon-mqtt%2Finsteon-mqtt-master%2Finsteon_mqtt%2Flog.py

    # Force the logging system to use our custom logger class, then restore whatever was set when we're done.
    logging.setLoggerClass(Logger)
    myLogger = logging.getLogger(name)
    myLogger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename=filepath)
    fh.setLevel(logging.DEBUG)
    fmt = '[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s'
    datefmt = "%Y-%m-%d %H:%M:%S %z"
    formatter = logging.Formatter(fmt,datefmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    myLogger.addHandler(sh)
    myLogger.addHandler(fh)

    return myLogger