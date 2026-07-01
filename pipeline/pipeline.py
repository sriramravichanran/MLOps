from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessing 
from src.model_training import ModelTraining 
from utils.utils import read_yaml 
from config.config_paths import*


if __name__ == "__main__":
    #1. Data Ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run() 

    #2. Data Preprocessing
    data_processor = DataProcessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH) 
    data_processor.process()

    #3. Model Training
    model_trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH,MODEL_OUTPUT_PATH)
    model_trainer.run()
    










