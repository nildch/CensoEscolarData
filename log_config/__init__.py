import logging
import logging.handlers

logger = logging.getLogger("CensoEscolarAPI")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


stream = logging.StreamHandler()
stream.setFormatter(formatter)
logger.addHandler(stream)


file_handler = logging.handlers.RotatingFileHandler(
    "api.log", maxBytes=200000, backupCount=3
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
