import logging
import os
from datetime import datetime

# Create Logs Directory (only if not exists)
LOG_DIR = "LOGS"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE)

# LOGGING CONFIGURATION
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format= "[ %(asctime)s ] %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Create Logger Object 
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger