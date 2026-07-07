import logging
import os
from datetime import datetime

LOG_DIR = "LOGS"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)

    # console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)


    return logger