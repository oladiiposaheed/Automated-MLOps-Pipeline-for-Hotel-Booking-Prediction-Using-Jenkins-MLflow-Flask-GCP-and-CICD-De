import os
import yaml
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError('File not found in the path')
    
        # Else 
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info('Successfully read the yaml file')
            return config
        
    except Exception as e:
        logger.error('Error occuured while reading yaml file')
        raise CustomException('Failed to read yaml file', e)
 
    
# Loading the data
def load_data(path):
    try:
        logger.info('Loading Data')
        return pd.read_csv(path)
    
    except Exception as e:
        logger.error(f'Error Loading the Data: {e}')
        raise CustomException('Failed to load data', e)
    