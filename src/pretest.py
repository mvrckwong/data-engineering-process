import pandas as pd

from pathlib import Path
from pydantic import BaseModel, ValidationError, validator
from typing import List
from datetime import datetime
from loguru import logger

from config_paths import LOGS_PATH, DATA_RAW_PATH

# Setup the logging
logger.add(LOGS_PATH / f"{Path(__file__).stem}.log", rotation="7 days", level="DEBUG")

class UserCheckIn(BaseModel):
    user: str
    timestamp: datetime
    hours: float
    project: str

    @validator('user', 'project')
    def must_not_be_empty(cls, v):
        if not v:
            raise ValueError('must not be empty')
        return v

    @validator('hours')
    def must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('must be non-negative')
        return v

    # @validator('timestamp', pre=True)
    # def parse_timestamp(cls, v):
    #     datetime_formats = [
    #         "%Y-%m-%d %H:%M:%S %Z",  # e.g., 2019-09-27 00:00:00 UTC
    #         "%m/%d/%Y %I:%M %p",     # e.g., 09/27/2019 12:00 AM
    #         "%d %B %Y %H:%M"         # e.g., 26 сентября 2019 00:00
    #     ]
        
    #     for fmt in datetime_formats:
    #         try:
    #             return datetime.strptime(v, fmt)
    #         except ValueError:
    #             continue
    #     raise ValueError(f"timestamp {v} is not in a recognized format")

def main(file_path: str) -> List[UserCheckIn]:
    """
    Validates each row of the dataset against the DailyCheckin Pydantic model.
    
    Args:
    - file_path: Path to the CSV file containing the data.
    
    Returns:
    - A list of DailyCheckin instances for valid rows.
    
    Raises:
    - Prints validation errors for rows that do not conform to the model.
    """
    data = pd.read_csv(file_path)
    
    valid_data = []
    for index, row in data.iterrows():
        try:
            checkin = UserCheckIn(
                user=row['user'],
                timestamp=row['timestamp'],
                hours=row['hours'],
                project=row['project']
            )
            valid_data.append(checkin)
        except ValidationError as e:
            logger.debug(f"Row {index} error: {e}")

    return valid_data


# Validate the data
if __name__ == "__main__":
    logger.debug(main(DATA_RAW_PATH / 'dailycheckins.csv'))