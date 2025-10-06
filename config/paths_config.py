import os # Imports the 'os' module, essential for file path manipulation and system-level operations.

# *----------------- Data Ingestion Paths and Setup ---------------*
# Defines the base directory where all raw and split data artifacts will be stored.
RAW_DIR = "artifacts/raw"

# Ensures the 'artifacts/raw' directory exists; creates it if it doesn't, preventing file-saving errors later.
os.makedirs(RAW_DIR, exist_ok=True)

# Constructs the absolute path for the *initial, unsplit* raw dataset file (e.g., artifacts/raw/raw.csv).
RAW_FILE_PATH = os.path.join(RAW_DIR, 'raw.csv')

# Constructs the absolute path for saving the cleaned or processed *training* dataset file.
TRAIN_FILE_PATH = os.path.join(RAW_DIR, 'train.csv')

# Constructs the absolute path for saving the cleaned or processed *testing* dataset file.
TEST_FILE_PATH = os.path.join(RAW_DIR, 'test.csv')

# *----------------- Configuration Path ---------------*
# Defines the relative path to the main YAML configuration file used to store project settings and hyperparameters.
CONFIG_PATH = 'config/config.yaml'


# ------------------- Data Processing ------------------
PROCESSED_DIR = 'artifacts/proccessed'
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, 'processed_train.csv')
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, 'processed_test.csv')


# -------------------- Model Training --------------------
MODEL_OUTPUT_PATH = 'artifacts/models/lgbm_model.pkl'
