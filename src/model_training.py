import lightgbm as lbg
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score
from src.logger import get_logger
from src.exception import CustomException
import os
import sys
import pandas as pd
from config.config_paths import *
from config.model_params import *
import joblib
from utils.utils import read_yaml, load_data
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV

logger = get_logger(__name__)


class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_data_and_split_data(self):
        try:
            logger.info(f"Loading data from: {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from: {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['Class'])
            y_train = train_df['Class']


            X_test = test_df.drop(columns=['Class'])
            y_test = test_df['Class']

            logger.info("Data Loading & Splitting is completed sucessfully and ready for model training....!")
            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error("Error while Data Loading & Splitting for model training")
            raise CustomException("Failed to Load data  & split data for model training", sys)
        
    def train_model_lgbm(self, X_train, y_train):       
        try:
            logger.info(f"Initializing the Model")

            lgbm_cls_model = lbg.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our HyperParameter Tunning...")
            random_search = RandomizedSearchCV(
                estimator = lgbm_cls_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv = self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params["scoring"]
            )

            logger.info("Started - Model Training with HyperParameter Tunning...!")
            random_search.fit(X_train, y_train)
            logger.info("HyperParameter Tunning is Completed Successfully...!")

            best_params = random_search.best_params_
            best_estimator_of_lgbm_model = random_search.best_estimator_

            logger.info(f"Best Parameters are: {best_params}")

            return best_estimator_of_lgbm_model
        
        except Exception as e:
            logger.error("Error while Training the Model & HyperParamater Tunning")
            raise CustomException("Failed to Train the model & HyperParamater Tunning", sys)
        
    def evaluate_model(self,model, X_test, y_test):
        try:
            logger.info("Started with Evaluating the Model")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy Score: {accuracy}")
            logger.info(f"precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"F1: {f1}")

            return {
                "Accuracy Score": accuracy,
                "Precision":precision,
                "Recall": recall,
                "F1": f1
            }

        except Exception as e:
            logger.error("Error while Evaluating the Model")
            raise CustomException("Failed to Evaluate the Model", sys)
        
    def save_model(self, model):
        try:
            # Creating a Directory 
            os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH),exist_ok=True)
            logger.info("Saving the Model")

            joblib.dump(model, self.model_output_path)
            logger.info(f"Successfully Model is Saved into: {self.model_output_path}")

        except Exception as e:
            logger.error("Error Saving the Model")
            raise CustomException("Failed to Saving the Model", sys)
        
    def run(self):
        try:
            # 1. Load & Split the Data
            logger.info("Started our Model Training Pipleing..")
            X_train, y_train, X_test, y_test = self.load_data_and_split_data()

            # 2. train_model_lgbm
            best_estimator_of_lgbm_model = self.train_model_lgbm(X_train, y_train)

            # 3. Evaluating the Model
            metrics = self.evaluate_model(best_estimator_of_lgbm_model, X_test, y_test)

            # 4. Saving the Model
            self.save_model(best_estimator_of_lgbm_model)

            logger.info("Model Training Successfully Completed....!")

        except Exception as e:
            logger.error("Error in Model Training Pipeline")
            raise CustomException("Failed in Model Training Pipeline", sys)    
        

if __name__ == "__main__":
    model_trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_PATH)
    model_trainer.run()