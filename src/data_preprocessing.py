from utils.utils import read_yaml, load_data
import os
from src.exception import CustomException
from src.logger import get_logger
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
from imblearn.over_sampling import SMOTE
from config.config_paths import *
from sklearn.impute import SimpleImputer
import sys

logger = get_logger(__name__)

class DataProcessing():
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def process_the_data(self, df):
        try:
            logger.info("Preprocessing step is Started....!")
            # 1. Droping the Duplicates
            df.drop_duplicates(inplace=True)
            logger.info("Duplicates Removed....!")

            # 2. Seggregating Numerical Columns
            numerical_columns = [
                col for col in self.config_path["data_preprocessing"]["numerical_columns"] 
                if col!="Class"
            ]
            
            logger.info("Duplicates Removed....!")
            
            # 3. Coverting Time (Seconds) -> Hour of Day
            df['Time'] = (df['Time'] // 3600) % 24
            logger.info("Time column coverted into Hour of the Day")

            # 4. Applying the Skewness
            logger.info("Skewness Process -> Started")
            skewness_thresold = self.config_path["data_preprocessing"]["skewness_thresold"]
            skewness = df[numerical_columns].apply(lambda x:x.skew())
            
            for col in skewness[skewness > skewness_thresold].index:
                min_value = df[col].min()

                if min_value <= -1:
                    continue
                df[col] = np.log1p(df[col])
            return df

        except Exception as e:
            logger.error(f"Error while preprocess steps: {e}")
            raise CustomException("Failed to perform Preprocessing",sys)
        
    def balance_the_data(self, df):
        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop('Class',axis=1)
            y = df['Class'].values.ravel().astype(int)
            
            # Imputer that replaces NAN's with the mean
            imputer = SimpleImputer(strategy='mean')
            X_imputed = imputer.fit_transform(X)

            print(df["Class"].value_counts())

            smote = SMOTE(random_state=42, k_neighbors=1)

            X_res, y_res = smote.fit_resample(X_imputed,y)

            balanced_df = pd.DataFrame(X_res, columns=X.columns)
            balanced_df["Class"] = y_res

            logger.info("Imbalanced Data is handled Successfully...")
            return balanced_df

        except Exception as e:
            logger.error(f"Error while Handling Imbalaned Data: {e}")
            raise CustomException("Failed to Handle Imbalaned Data:",sys)
    
        
    def features_selection(self, df):
        try:
            # 1. Seggregating X & Y
            logger.info("Started with Feature Selection Process....")

            X = df.drop('Class', axis=1)
            y = df['Class']

            # 2. Training Model
            model_lr = LogisticRegression(
                max_iter=2000,
                class_weight='balanced',
                solver='liblinear'
            )

            model_lr.fit(X, y)

            # 3. Feature Importance
            feature_importances = np.abs(model_lr.coef_[0])

            df_feature_importances = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importances
            })

            top_features_importance_df = df_feature_importances.sort_values(
                by="importance",
                ascending=False
            )

            num_of_features_to_select = self.config_path[
                "data_preprocessing"
            ]["no_of_features"]

            top_features = top_features_importance_df[
                'feature'
            ].head(num_of_features_to_select).values

            logger.info(f"Features Selected: {top_features}")

            # Selected features
            selected_df = df[top_features.tolist()].copy()

            # IMPORTANT -> Add target column back
            selected_df["Class"] = y.values

            logger.info("Feature Selection is done Successfully....")

            return selected_df

        except Exception as e:
            logger.error(f"Error while doing feature selection step {e}")
            raise CustomException("Error while Feature Selection", sys)
        
        
    
    def save_data(self, df, file_path):
        try:
            logger.info("Saving data from preprocessed folder....!")

            df.to_csv(file_path, index=False)

            logger.info(f"Data Saved Successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error while saving the preprocessed data {e}")
            raise CustomException("Error while saving preprocessed data", sys)

    def process(self):
        try:
            logger.info("Loading data from RAW Directory")

            # 1. Loading the DataFrame
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # 2. Processing the Data
            train_df = self.process_the_data(train_df)
            test_df = self.process_the_data(test_df)

            # 3. Handling the Imbalanced Data
            train_df = self.balance_the_data(train_df)
            # test_df = self.balance_the_data(test_df)

            # 4. Feature Selection
            train_df = self.features_selection(train_df)

            # Get selected feature columns
            selected_columns = train_df.columns.tolist()

            # Remove target column from features list
            selected_columns.remove("Class")

            # Keep same feature columns in test data + target column
            test_df = test_df[selected_columns + ["Class"]]

            # Save processed data
            self.save_data(train_df, PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, PROCESSED_TEST_FILE_PATH)

            logger.info("Data Preprocessing is completed Successfully....!")

        except Exception as e:
            logger.error(f"Error during applying Preprocessing Steps: {e}")
            raise CustomException("Error during Data Preprocessing",sys)

if __name__ == "__main__":

    data_processor = DataProcessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_processor.process()