import streamlit as st
import pandas as pd

from pathlib import Path
from loguru import logger
from typing import List, Tuple

from config_paths import LOGS_PATH, DATA_PROCESS_PATH
import configs as CONFIGS

# Setup the logging
logger.add(LOGS_PATH / f"{Path(__file__).stem}.log", rotation="7 days", level="DEBUG")

@st.cache_data
def load_data(filepath:Path) -> pd.DataFrame:
    """Load and preprocess the check-in data."""
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    df = pd.read_parquet(filepath)
    return df

@st.cache_data
def load_data_from_db() -> pd.DataFrame:
    """Load data from the database."""
    # Database Credentials
    # db_creds_var = ['DB_USER', 'DB_PW', 'DB_HOST', 'DB_NAME']
    # for var in db_creds_var:
    #     if getenv(var)=='':
    #         raise ValueError(f'Environment variable {var} not set')
    
    # # Database Connection URL and Create the SQLAlchemy engine
    # db_connect_url = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PW')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}?sslmode=require"
    # db_engine = create_engine(db_connect_url)
    
    # Connect to SQLAchemy Engine
    db_engine = CONFIGS.db_connection()
    
    # Query the table and load it into a Pandas DataFrame
    return pd.read_sql_table(CONFIGS.CURRENT_TABLE, db_engine)


@logger.catch
def calculate_summary_statistics(user_data:pd.DataFrame) -> Tuple[int, int, list]:
    """Calculate and return summary statistics for the user data."""
    total_hours = user_data['project_hours'].sum()
    average_hours_per_project = user_data.groupby('project_name')['project_hours'].mean().to_dict()
    checkin_count = user_data.shape[0]
    return total_hours, checkin_count, average_hours_per_project 

@logger.catch
def main() -> None:
    """Main function for the Streamlit app."""
    
    # Try connecting to the database
    # Else, load the data from the data directory
    try:
        df = load_data_from_db()
        logger.info('Got data from the database.')
    except:
        df = load_data(DATA_PROCESS_PATH / f'{CONFIGS.CURRENT_TABLE}.parquet')
        logger.info('Got data from the raw data directory.')
    
    # Get the list of users based on pandas data
    users:List[str] = [''] + df['user_name'].unique().tolist()
    
    # Headers
    st.header('User Check-In')
    st.write('\n')
    
    # Selection Box and Submit Form
    user_name = st.selectbox('Select User Name:', users)
    submit = st.button('Submit')
    st.write('\n')
    
    # Check if all three exists before showing the data.
    user_data = df[df['user_name'] == user_name]
    if submit and user_name and not user_data.empty:
        logger.info(f'Selected: {user_name}.')
        
        # User Charts
        with st.expander('User Charts', expanded=True):
            
            project_data = user_data[user_data['is_project'] == True]
            non_project_data = user_data[user_data['is_project'] == False]

            # Group the filtered data by 'project_name' and sum 'project_hours'
            hours_per_project = project_data.groupby('project_name')['project_hours'].sum()
            hours_per_nonproject = non_project_data.groupby('project_name')['project_hours'].sum()
            
            # Visualize the data
            st.subheader('Number of hours logged per project')
            st.bar_chart(hours_per_project)
            st.subheader('Number of hours logged per non-project')
            st.bar_chart(hours_per_nonproject)
            
            # Visualization: Hours Logged Over Time
            st.subheader('Number of hours logged over time')
            hours_over_time = user_data.groupby('project_date')['project_hours'].sum()
            st.line_chart(hours_over_time)
            
        # User Datas
        with st.expander('User Data', expanded=False):
            # Calculate the following
            total_hours, checkin_count, avg_hours_per_project = calculate_summary_statistics(user_data)

            # Create a dictionary with the statistics
            stats = {
                "Total Hours Logged": f"{total_hours:.2f}",
                "Total Number of Check-Ins (Rows)": f"{checkin_count:.2f}",
            }

            # Convert the dictionary to a DataFrame for displaying as a table
            st.subheader('Summary Statistics:')
            stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Hours'])
            st.table(stats_df)
            
            st.subheader('Average Hours per Project:')
            avg_hours_df = pd.DataFrame([(project, f"{hours:.2f}") for project, hours in avg_hours_per_project.items()], columns=['Project', 'Average Hours'])
            st.table(avg_hours_df)
    
    return True
    

if __name__ == "__main__":
    if main():
        logger.info(f'Running {Path(__file__).name} successful!')