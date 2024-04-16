import pandas as pd
from loguru import logger
from pathlib import Path

from config_paths import DATA_RAW_PATH, DATA_PROCESS_PATH, LOGS_PATH
import configs as CONFIGS

# Setup the logging
logger.add(LOGS_PATH / f"{Path(__file__).stem}.log", rotation="7 days", level="DEBUG")

""" TODO:
CHECK FOR THE FOLLOWING
- Data Type
- Data Format (if date, is it YYYY-MM-DD?. if float, how many decimals?)
- Nulls, Nans, Blanks, and Invalid
- Base, Ceiling and Zeros

- Replace Columns if not clear (use snake_case)
"""

def rename_df_cols(input_df:pd.DataFrame) -> pd.DataFrame:
    """
    Renames the columns of the input dataframe according to the standard mapping provided in the standard_cols dictionary.
    """
    standard_cols = {
        'user': 'user_name', 
        'timestamp': 'project_timestamp',
        'hours': 'project_hours',
        'project': 'project_name'
    }
    
    return input_df.rename(columns=standard_cols, errors='raise')

def transform_df_cols_user(input_df:pd.DataFrame) -> pd.DataFrame:
    """ Transform user_name columns """
    current_col = 'user_name'
    
    # Drop rows where the  column has NaN values
    output_df = input_df.dropna(subset=[current_col])
    
    # Convert the column to string type
    output_df[current_col] = output_df[current_col].astype(str)
    
    # Transform the data
    output_df[current_col] = output_df[current_col].str.strip()
    output_df[current_col] = output_df[current_col].str.lower()
    
    return output_df


def transform_df_cols_hours(input_df:pd.DataFrame) -> pd.DataFrame:
    """ Transform project_hours columns """
    current_col = 'project_hours'
    
    # Convert the column to string type
    input_df[current_col] = input_df[current_col].astype(float)
    
    # # Round the numbers to a consistent number of decimal places, e.g., 2 decimal places.
    # input_df[current_col] = input_df[current_col].round(2)

    # # If you need the numbers to be strings with two decimal places (for display purposes)
    # input_df[current_col] = input_df[current_col].apply(lambda x: f'{x:.2f}').astype(float)
    
    return input_df


def transform_df_cols_timestamp(input_df:pd.DataFrame) -> pd.DataFrame:
    """ Transform user_name columns """
    current_col = 'project_timestamp'
    
    # Filter Columns that have dots
    filtered_df = input_df[input_df[current_col].str.contains('.', regex=False)]
    filtered_df[current_col] = filtered_df[current_col].str.split('.', expand=True)[0] + ' UTC'

    # Update both columns
    input_df.update(filtered_df)
    input_df[current_col] = pd.to_datetime(input_df[current_col], errors='coerce', utc=True)
    
    # Fitler further
    # TODO: Remove this once, the data properly processed.
    input_df = input_df[~input_df['project_timestamp'].isna()]
    
    # Split date and time
    input_df['project_date'] = input_df['project_timestamp'].dt.date.astype('datetime64[ns]')
    input_df['project_time'] = input_df['project_timestamp'].dt.time
    input_df.drop(columns=['project_timestamp'], inplace=True)
    
    return input_df.reset_index(drop=True)


def insert_df_cols(input_df:pd.DataFrame) -> pd.DataFrame:
    
    # Create a new column 'is_project' that checks for the substring 'project'
    input_df['is_project'] = input_df['project_name'].str.contains('project')

    # Replace NaN values with False in 'is_project' column (if any NaNs are present)
    input_df['is_project'] = input_df['is_project'].fillna(False)

    # Ensure that 'is_project' is of boolean dtype
    input_df['is_project'] = input_df['is_project'].astype(bool)
    
    return input_df

def main() -> bool:
    
    # Load the data
    df = pd.read_csv(DATA_RAW_PATH / f'{CONFIGS.CURRENT_TABLE}.csv')
    logger.debug('Data loaded successfully.')
    
    # Rename the columns
    df = rename_df_cols(df)
    logger.debug('Columns renamed successfully.')
    
    # Transform the dataframe
    df = transform_df_cols_user(df)
    df = transform_df_cols_hours(df)
    df = transform_df_cols_timestamp(df)
    logger.debug('Data transformed successfully.')
    
    # Insert datas
    df = insert_df_cols(df)
    
    # Reorder the columns
    df = df[['user_name', 'project_date', 'project_time', 'project_hours', 'project_name', 'is_project']]
    logger.debug('New columns added and reordered.')
    
    # Save the processed data
    df.to_parquet(DATA_PROCESS_PATH / f'{CONFIGS.CURRENT_TABLE}.parquet', index=False)
    return True


if __name__ == "__main__":
    if main():
        logger.info(f'Running {Path(__file__).name} successful!')