import logging


def getlog(nm):
    # create custom logger
    logger = logging.getLogger(nm)
    # reading content from properties file
    f = open("properties.txt", "r")
    if f.mode == "r":
        loglevel = f.read()
    if loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    elif loglevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    # Creating Format
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    # Creating Handlers
    file_handler = logging.FileHandler("test.log")
    # Adding Formatters to Handlers
    file_handler.setFormatter(formatter)
    # Adding Handlers to logger
    logger.addHandler(file_handler)
    return logger
