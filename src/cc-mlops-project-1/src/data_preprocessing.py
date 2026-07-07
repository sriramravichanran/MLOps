from utils.utils import read_yaml, load_data
import os
from src.exception import CustomException
from src.logger import get_logger
import numpy as np


logger = get_logger(__name__)


class DataPreprocessing():
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def process_the_data(self,df):
        try:
            logger.info("Preprocessing step is started...!")

            #1. Droping the Duplicates
            df.drop_duplicates(inplace=True)
            logger.info("Duplicates Removed...!")

            #2.Seggregating Numerical Columns
            numerical_columns = self.config_path["data_preprocessing"]["numerical_columns"] 
            logger.info("Duplicates Removed..!")

            #3. Converting Time (Seconds) -> Hour of Day
            df['Time'] = (df['Time'] // 3600) % 24
            logger.info("Time column converted into Hour of the day")

            #4. Applying the skewness
            logger.info("Skewness Process -> Started")
            skewness_threshold = self.config_path["data_preprocessing"]["skewness_threshold"]
            skewness = df[numerical_columns].apply(lambda x:x.skew())
            
            for col in skewness[skewness > skewness_threshold].index:
                if (df[col] > 0).all():df[col] = np.log1p(df[col])
            return df
    
        except Exception as e:
            logger.error(f"Error while preprocess steps: {e}")
            raise CustomException("Failed to perform preprocessing", e)