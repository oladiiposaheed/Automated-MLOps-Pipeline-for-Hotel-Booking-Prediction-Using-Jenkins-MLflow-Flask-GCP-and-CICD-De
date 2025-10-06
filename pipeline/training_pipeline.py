from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.training_model import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *

# Data Ingestion
if __name__ == '__main__':
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
    
# Data Processing
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
    
# Model Training
if __name__ == '__main__':
    
    #Create an object for ModelTraining
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()