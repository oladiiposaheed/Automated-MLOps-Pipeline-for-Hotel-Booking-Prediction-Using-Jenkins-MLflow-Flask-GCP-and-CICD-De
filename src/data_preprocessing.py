import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        self.config = read_yaml(config_path)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess_data(self, df):
        try:
            logger.info('Starting Data Preprocessing')
            
            logger.info('Dropping the columns')
            
            # Drop Unnamed: 0 and Booking_ID columns
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True)
            
            # Drop duplicate
            df.drop_duplicates(inplace=True)
            
            # Extract all categorical columns from config yaml
            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']            
            
            logger.info("Applying Label Encoding")
            
            # ----- Perform Label Encoding ------
            
            #Dictionary to store the fitted encoders for inverse transformation/mapping
            encoder_mappings = {}

            le = LabelEncoder()
            mappings={}

            for col in cat_cols:
                df[col] = le.fit_transform(df[col])
                encoder_mappings[col] = {label:code for label,code in zip(le.classes_ , le.transform(le.classes_))}

            logger.info("Label Mappings are : ")
            for col,mapping in encoder_mappings.items():
                logger.info(f"{col} : {mapping}")
                
            
            # Perform Skewness on numerical columns    
            logger.info('Perform Skewness Handling')
            
            skew_threshold = self.config['data_processing']['skewness threshold']
            
            
            skewness = df[num_cols].apply(lambda x: x.skew())
            
            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])
                
            return df
        
        except Exception as e:
            logger.error(f'Error Occurred During Preprocessing Data: {e}')
            raise CustomException('Error Occurred During Preprocessing', e)
            
    # Method for Handling Imbalanced Data        
    def balance_data(self, df):
        try:
            logger.info('----- Handling Imbalanced Data ------')
            X = df.drop(columns = 'booking_status')
            y = df['booking_status']
            
            smote = SMOTE(random_state=43)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled
            
            logger.info('Data Balanced Successfully')
            
            return balanced_df
            
        except Exception as e:
            logger.error(f'Error Occurred During Balancing Data: {e}')
            raise CustomException('Error Occurred During Balancing', e)
        
    
    # Perform Feature Selection    
    def select_features(self, df):
        try:
            logger.info('----- Performing Faturing Seelction Step -----')
            
            X = df.drop(columns = 'booking_status')
            y = df['booking_status']
            
            model = RandomForestClassifier(random_state=43)
            model.fit(X, y)
            
            feature_importance = model.feature_importances_
            
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })
            best_features_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
            
            num_features_to_select = self.config['data_processing']['no_of_features']
            
            best_10_features = best_features_importance_df['feature'].head(num_features_to_select).values
            
            logger.info(f'Best Features Selected: {best_10_features}')
            
            #best_10_df = df(best_10_features.tolist() + ['booking_status'])
            best_10_df = df[best_10_features.tolist() + ['booking_status']]  
            
            logger.info('Feature Selection Completed Successfully')
            
            return best_10_df
        
        except Exception as e:
            logger.error(f'Error Occurred During Feature Selection: {e}')
            raise CustomException('Error Occurred During Feature Selection', e)
        
        
    # Save Data
    def save_data(self, df, file_path):
        try:
            logger.info('Saving Processed Data inside Processed Folder')
            
            df.to_csv(file_path, index=False)
            
            logger.info(f'Data Saved Successfully to {file_path}')
            
        except Exception as e:
            logger.error(f'Error Occurred During Saving Data: {e}')
            raise CustomException('Error Occurred During Saving Data', e)
        
    
    def process(self):
        try:
            logger.info('Loading Data from Raw Directory')
            
            # Load train dataframe and test dataframe
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
       
            #Perform preprocessing on train df and test df
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            
            # Perform Balancing Dataset
            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)
            
            #Select the Features
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            
            logger.info('Data Preprocessing Completed Successfully')
            
        except Exception as e:
            logger.error(f'Error Occurred During Data Preprocessing Pipeline: {e}')
            raise CustomException('Error Occurred During Data Preprocessing Pipeline', e)
        

if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()