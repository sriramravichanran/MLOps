import sys
import pandas as pd
import os
from sklearn.model_selection import train_test_split


from config.config_paths import *
from src.logger import get_logger
from src.exception import CustomException
from google.cloud import storage
from utils.utils import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR,exist_ok=True)
        logger.info(f"Data Ingestion started --- {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp_bucket(self):
        try:
            client = storage.Client()

            print(client)

            buckets = list(client.list_buckets())

            for i in buckets:
                print(i)

                
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"CSV file is successfully downloaded to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error while downloading CSV file: {e}")
            raise CustomException("Failed to download CSV file",sys)
        
        
    def data_split_to_train_test(self):
      try:
          logger.info("Started with splitting the data into Train & Test Split..")
          dataset = pd.read_csv(RAW_FILE_PATH)
          train_data, test_data = train_test_split(dataset, test_size =1 - self.train_test_ratio, random_state = 42)

          train_data.to_csv(TRAIN_FILE_PATH, index=False)
          test_data.to_csv(TEST_FILE_PATH, index=False)

          logger.info(f"Train data is Saved to {TRAIN_FILE_PATH}")
          logger.info(f"Test data is Saved to {TEST_FILE_PATH}")
      
      except Exception as e:
           logger.info("Error while splitting the raw data into Train & Test Split")
           raise CustomException("Failed to split the rawdata into Train and Test Split...!", sys)

    
    def run(self):
        try:
            logger.info("Data Ingestion is Started...!")
            
            self.download_csv_from_gcp_bucket()

            logger.info("Data is downloaded Successfully from GCP")

            self.data_split_to_train_test()
            logger.info("Raw data is splitted into Train and Test succeessfully...")


            logger.info("Data Ingestion is Successfully Completed...!")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")

        finally:
            logger.info("Data Ingestion Completed")


if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()
