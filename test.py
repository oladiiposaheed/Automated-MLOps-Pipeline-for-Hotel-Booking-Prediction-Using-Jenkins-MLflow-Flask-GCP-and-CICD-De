from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide(a, b):
    try:
        res = a / b
        logger.info('Divide numbers')
        return res
    
    except Exception as e:
        logger.error('Error Successfully occur')
        raise CustomException('Custom Division Error', sys)
    
if __name__ == '__main__':
    try:
        logger.info('Starting the Program')
        divide(5, 0)
    
    except CustomException as ce:
        logger.error(str(ce))