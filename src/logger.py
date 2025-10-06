import os
import logging
from datetime import datetime

# Define the name of the directory where logs will be stored.
LOGS_DIR = "logs"
# Create logs directory if it doesn't exist
if not os.path.exists(LOGS_DIR): # Check if logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True) # Create logs directory if it doesn't exist

# Create a log file with the current date and time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Current date and time in format YYYY-MM-DD_HH-MM-SS
LOG_FILE = os.path.join(LOGS_DIR, f'log_{timestamp}.log') # Log file name with timestamp e.g., log_2023-10-05_14-30-00.log

# Configure logging settings, why INFO level? because it captures all levels above it (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(
    filename= LOG_FILE, # Log file path
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', # Log message format with timestamp, log level, logger name, and message e.g., 2023-10-05 14:30:00, INFO, logger_name, This is a log message
    level=logging.INFO, # Set the logging level to INFO  ie. capture INFO and above i.e., WARNING, ERROR, CRITICAL will be captured as well 
    
)

# Create a logger function to get the logger instance
def get_logger(name: str) -> logging.Logger:
    """Function to get the logger instance"""
    logger = logging.getLogger(name) # Get the logger instance with the specified name
    logger.setLevel(logging.INFO) # Set the logging level to INFO
    return logger # Return the logger instance