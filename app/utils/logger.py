import logging
from app.utils.db_logger import DBHandler
from app.models.log import Log

# Setup the logger
logger = logging.getLogger("task_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("task_api.log")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")


# DB Handler - Custom Handler for DB logging
db_handler = DBHandler()
db_handler.setFormatter(formatter)
logger.addHandler(db_handler)
