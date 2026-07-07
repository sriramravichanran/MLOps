import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#------------------------Data Ingestion-------------------
RAW_DIR = os.path.join(BASE_DIR, "artifacts", "raw")
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv") # artifacts/raw/raw.csv
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv") # artifacts/raw/train.csv
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv") # artifacts/raw/test.csv

CONFIG_PATH =  os.path.join(BASE_DIR, "config", "config.yaml")


# What to download -> Dataset
# Where to download -> Config_paths
# How to open and read the dataset -> Utils -> file

#--------------- Data Preprocessing------------------
PROCESSED_DIR = os.path.join(BASE_DIR, "artifacts", "processed_data")
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR, "processed_train_data.csv") # artifacts/processed_data/processed_train_data.csv
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR, "processed_test_data.csv") # artifacts/processed_data/processed_test_data.csv


#---------------Model Training------------------
MODEL_OUTPUT_PATH = "artifacts/models/lg_model.pkl" # artifacts/models/lg.model.pkl

