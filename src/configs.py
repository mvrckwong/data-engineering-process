from os import getenv
from sqlalchemy import create_engine
from dotenv import load_dotenv
from config_paths import PROJECT_PATH
from typing import Final

CURRENT_TABLE:Final = 'dailycheckins'

# Standard configuration 
env_path = PROJECT_PATH / '.env'
if not env_path.exists():
    raise FileNotFoundError(f"Environment file {env_path} not found!")

def db_connection():
    """ Establish a connection to a PostgreSQL database using the provided connection URL. """
    load_dotenv(env_path)
    
    db_creds_var = ['DB_USER', 'DB_PW', 'DB_HOST', 'DB_NAME']
    for var in db_creds_var:
        if getenv(var)=='':
            raise ValueError(f'Environment variable {var} not set')
    
    # Database Connection URL and Create the SQLAlchemy engine
    connect_url = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PW')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}?sslmode=require"
    engine = create_engine(connect_url)
    return engine


if __name__ == "__main__":
    None