import os
import pandas as pd
from src.exception import CustomException
from src.logger import get_logger
import yaml
import sys
from utils.utils import read_yaml
from utils.utils import read_yaml, load_data

logger = get_logger(__name__)

# Operations for YAML file

# Read yaml file
def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File is not present in the path")
        
        with open(file_path, 'r') as read_yaml_file:
            config = yaml.safe_load(read_yaml_file)
            logger.info("Successfully YAML file reading operation is done...")
            return config
    except Exception as e:
        logger.error("Error while reading YAML file..")
        raise CustomException("Failed to Read the file",sys)
    
# Loading Data
def load_data(path):
    try:
        df = pd.read_csv(path)
        logger.info(f"Data loaded Successfully from path: {path}")
        return df
    except Exception as e:
        logger.error("Error while loading the Data")
        raise CustomException("Failed to load the Data",e)