import pandas as pd
from pathlib import Path
from loguru import logger

from config_paths import LOGS_PATH, DATA_PROCESS_PATH
import configs as CONFIGS

# Setup the logging
logger.add(LOGS_PATH / f"{Path(__file__).stem}.log", rotation="7 days", level="DEBUG")

@logger.catch
def main() -> None:
    """
    Setup the environment, establish connection, read CSV file into a DataFrame, and insert DataFrame into PostgreSQL table.
    This function does not take any parameters and returns None.
    """
    
    # Establish Connection
    db_engine = CONFIGS.db_connection()
    logger.info('Connection to database successful!')
    
    # Path to your CSV file
    file_path =  DATA_PROCESS_PATH / 'dailycheckins.parquet'

    # Read CSV file into a DataFrame and Insert DataFrame into PostgreSQL table
    df = pd.read_parquet(file_path)
    df.to_sql('dailycheckins', db_engine, if_exists='replace', index=False)
    logger.info('Ingest to database successful!')
    
    return True


if __name__ == "__main__":
    if main():
        logger.info(f'Running {Path(__file__).name} successful!')