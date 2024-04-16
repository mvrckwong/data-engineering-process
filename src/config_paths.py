from pathlib import Path

# Define the base path for your project
SRC_PATH:Path = Path(__file__).parent
PROJECT_PATH:Path = SRC_PATH.parent

# Define other paths relative to the base path
DATA_PATH:Path = PROJECT_PATH / 'data'
DATA_RAW_PATH:Path = DATA_PATH / 'raw'
DATA_PROCESS_PATH:Path = DATA_PATH / 'processed'

LOGS_PATH:Path = PROJECT_PATH / 'logs'
OUTPUT_PATH:Path = PROJECT_PATH / '.output'

if __name__ == "__main__":
    None