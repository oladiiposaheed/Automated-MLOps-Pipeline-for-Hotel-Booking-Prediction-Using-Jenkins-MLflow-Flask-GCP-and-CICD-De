import os
import pandas as pd
import joblib
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import mlflow
import mlflow.sklearn

# Initialize logger
logger = get_logger(__name__)

class ModelTraining:
    
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        
        #Initialize parameters
        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    # Load and split data
    def load_split_data(self):
        try:
            logger.info(f'Loading Data From {self.train_path}')
            train_df = load_data(self.train_path)
            
            logger.info(f'Loading Data From {self.test_path}')
            test_df = load_data(self.test_path)
            
            # Splitting the data
            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            
            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            
            logger.info('Data Splitted Successfully for Model Training')
            
            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f'Error Occurred while Loading the Data: {e}')
            raise CustomException('Failed to Execute the Model Pipeline', e)
        
        
    # Train the model on X_train, y_train
    def train_lgbm(self, X_train, y_train):
        try:
            # Instantiate the model
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])
            
            logger.info('Starting Hyperparameter Tuning')
            
            # Set Hyperparameter Tuning
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv = self.random_search_params['cv'],
                n_jobs = self.random_search_params['n_jobs'],
                verbose = self.random_search_params['verbose'],
                random_state = self.random_search_params['random_state'],
                scoring = self.random_search_params['scoring']
            )
            
            logger.info('Starting Model Training')
            
            # Train X_train, y_train
            random_search.fit(X_train, y_train)
            
            logger.info('Hyperparameter Tuning Completed')
            
            # Getting the best parameters best estimator i.e. best model 
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            
            logger.info(f'Best Parameters are: {best_params}')
        
            return best_lgbm_model
        
        
        except Exception as e:
            logger.error(f'Error Occurred while Training the Model: {e}')
            raise CustomException('Failed to Execute the Model Pipeline', e)
        
        
    # Evaluate the model
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info('Evaluating the Model')
            
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            recall  = recall_score(y_test, y_pred) # The recall is intuitively the ability of the classifier to find all the positive samples. The best value is 1 and the worst value is 0
            precision = precision_score(y_test, y_pred) # The precision is intuitively the ability of the classifier not to label as positive a sample that is negative. The best value is 1 and the worst value is 0.
            f1 = f1_score(y_test, y_pred) # The F1 score can be interpreted as a harmonic mean of the precision and recall, where an F1 score reaches its best value at 1 and worst score at 0
            
            logger.info(f'Accuracy Score: {accuracy}')
            logger.info(f'Recall Score: {recall}')
            logger.info(f'Precision Score: {precision}')
            logger.info(f'F1 Score: {f1}')
            
            return {
                'accuracy': accuracy,
                'recall': recall,
                'precision': precision,
                'f1': f1
            }
            
        except Exception as e:
            logger.error(f'Error Occurred while Evaluation the Model: {e}')
            raise CustomException('Failed to Execute the Model Pipeline', e)
        
        
    # Save the model
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            
            logger.info('Saving the model')
            joblib.dump(model, self.model_output_path)
            logger.info(f'Model saved to: {self.model_output_path}')
            
        except Exception as e:
                logger.error(f'Error Occurred while Evaluation the Model: {e}')
                raise CustomException('Failed to Execute the Model Pipeline', e)
            
    def run(self):
        try:
            
            with mlflow.start_run():
                
            
                logger.info('Starting Model Training Pipeline')
                
                logger.info('Starting MLFLOW eith Experimentation')
                
                logger.info('Logging the Training and Testing Dataset to MLFLOW')
                
                # Log the artifact
                mlflow.log_artifact(self.train_path, artifact_path='datasets')
                mlflow.log_artifact(self.test_path, artifact_path='datasets')
                
                X_train, y_train, X_test, y_test = self.load_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)
                
                #Log the model 
                logger.info('Logging Model into MLFLOW')
                mlflow.log_artifact(self.model_output_path)
                
                #Log Parameters and metrics of the model
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)
                
                logger.info('Logging Params and Metrics to MLFLOW')
                
                
                logger.info('Model Training Pipeline Successfully Completed')
                
        
        except Exception as e:
            logger.error(f'Error Occurred During Model Training Pipeline: {e}')
            raise CustomException('Failed to Execute the Model Pipeline', e)
            
# Test the Model Training
if __name__ == '__main__':
    
    #Create an object for ModelTraining
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()