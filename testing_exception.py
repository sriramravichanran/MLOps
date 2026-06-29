import sys
from src.exception import CustomException
from src.logger import get_logger

logger=get_logger(__name__)

try:
    a=10/2
    logger.info("Dividing two numbers")
    print(a)
except Exception as e:
    logger.error("Error occured while dividing 2 numbers.....")
    raise CustomException(e,sys)
