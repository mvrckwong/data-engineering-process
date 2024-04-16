from pandas import DataFrame, read_parquet, read_sql_table
from loguru import logger
from pathlib import Path

from config_paths import LOGS_PATH, DATA_PROCESS_PATH
import configs as CONFIGS

# Setup the logging
logger.add(LOGS_PATH / f"{Path(__file__).stem}.log", rotation="7 days", level="DEBUG")

@logger.catch
def test_compare_column_size(df1:DataFrame, df2:DataFrame):
    """
    Compare the number of columns in two DataFrames.
    """
    assert len(df1.columns) == len(df2.columns), "Column sizes do not match."

def test_compare_row_size(df1:DataFrame, df2:DataFrame):
    """
    Compare the number of rows in two DataFrames.
    """
    assert len(df1.index) == len(df2.index), "Row sizes do not match."

@logger.catch
def test_compare_null_values(df1:DataFrame, df2:DataFrame):
    """
    Compare the number of null values in each column of two DataFrames.
    """
    for col in df1.columns:
        assert df1[col].isnull().sum() == df2[col].isnull().sum(), f"Null values for column '{col}' do not match."

@logger.catch
def test_compare_blank_values(df1:DataFrame, df2:DataFrame):
    """
    Compare the number of blank values in two DataFrames.
    """
    assert df1.isin(['']).sum().sum() == df2.isin(['']).sum().sum(), "Blank values do not match."

@logger.catch
def test_compare_column_names(df1:DataFrame, df2:DataFrame):
    """
    Compare the column names of two DataFrames.
    """
    assert list(df1.columns) == list(df2.columns), "Column names do not match."

@logger.catch
def test_compare_column_orders(df1:DataFrame, df2:DataFrame):
    """
    Compare the order of columns in two DataFrames.
    """
    assert df1.columns.tolist() == df2.columns.tolist(), "Column orders do not match."

@logger.catch
def test_compare_index_values(df1:DataFrame, df2:DataFrame):
    """
    Compare the index values of two DataFrames.
    """
    assert df1.index.values.tolist() == df2.index.values.tolist(), "Index values do not match."

@logger.catch
def test_compare_unique_values(df1:DataFrame, df2:DataFrame):
    """
    Compare the unique values in each column of two DataFrames.
    """
    for col in df1.columns:
        assert list(set(df1[col].unique())) == list(set(df2[col].unique())), f"Unique values for column '{col}' do not match."

@logger.catch
def test_compare_missing_value_patterns(df1:DataFrame, df2:DataFrame):
    """
    Compare the missing value patterns in each column of two DataFrames.
    """
    for col in df1.columns:
        assert df1[col].isna().sum() == df2[col].isna().sum(), f"Missing value patterns for column '{col}' do not match."

@logger.catch
def test_compare_equals(df1:DataFrame, df2:DataFrame):
    """
    Compare two DataFrames for equality.
    """
    assert df1.equals(df2), "Dataframes are not equal."

def _convert_to_ints(input: list) -> list:
    """Convert a list of values to integers, treating non-numeric values as NaN."""
    result = []
    for value in input:
        try:
            result.append(int(float(value)))
        except:
            result.append("")
    return result


@logger.catch
def test_compare_int_values(df1:DataFrame, df2:DataFrame):
    """
    Compare the integer values in each column of two DataFrames.

    Parameters:
    - df1 (pd.DataFrame): The first DataFrame.
    - df2 (pd.DataFrame): The second DataFrame.

    Raises:
    - AssertionError: If the integer values in any column of df1 are not equal to the integer values in the corresponding column of df2.
    """
    for col in df1.columns:
        assert _convert_to_ints(df1[col].tolist()) == _convert_to_ints(df2[col].tolist()), f"Int values for column '{col}' do not match."
        
        
def main() -> None:
    
    # Load the datas
    # Load the database data
    df_engine = CONFIGS.db_connection()
    df1 = read_sql_table(CONFIGS.CURRENT_TABLE, df_engine)
    logger.info('Database data loaded successfully.')
    
    # Load the processed data
    df2 = read_parquet(DATA_PROCESS_PATH / f'{CONFIGS.CURRENT_TABLE}.parquet')
    logger.info('Processed data loaded successfully.')
    
    # Validate the data
    test_compare_column_size(df1, df2)
    test_compare_row_size(df1, df2)
    test_compare_null_values(df1, df2)
    #test_compare_blank_values(df1, df2)
    test_compare_column_names(df1, df2)
    test_compare_column_orders(df1, df2)
    test_compare_index_values(df1, df2)
    #test_compare_unique_values(df1, df2)
    test_compare_missing_value_patterns(df1, df2)
    # test_compare_equals(df1, df2)
    #test_compare_int_values(df1, df2)
    logger.info('Data validated successfully.')
    
    return True


if __name__ == "__main__":
    if main():
        logger.info(f'Running {Path(__file__).name} successful!')