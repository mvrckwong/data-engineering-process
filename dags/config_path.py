from pathlib import Path

# Define the base path for your project
DAGS_PATH:Path = Path(__file__).parent
PROJECT_PATH:Path = DAGS_PATH.parent

# Define other paths relative to the base path
DATA_PATH:Path = PROJECT_PATH / 'data'
LOGS_PATH:Path = PROJECT_PATH / 'logs'
OUTPUT_PATH:Path = PROJECT_PATH / '.output'
SRC_PATH:Path = PROJECT_PATH / 'src'

if __name__ == "__main__":
    None