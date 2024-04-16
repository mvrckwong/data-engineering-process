from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import config as CONFIG
from config_path import SRC_PATH

""" 
TODO:
Create the DAG for the following:
- Entire Datapipeline
- Clean or Preprocess Data
- Ingesting the Data (db)
- Testing the Data
- Delete the Data (db)
"""

# Entire Datapipeline
with DAG(
    "UserCheckin-DataPipeline",
    default_args=CONFIG.DEFAULT_ARGS,
    schedule_interval=None,
    catchup=False
    ) as dag:
    
        
    # Define the task within the DAG context
    run_prevalidate_batch = BashOperator(
        task_id="run_prevalidate_batch",
        bash_command = f"echo Hello World",
        dag=dag
    )
    
    # Define the task within the DAG context
    run_transform_batch = BashOperator(
        task_id="run_transform_batch",
        bash_command = f"echo Hello World",
        dag=dag
    )
    
    # Define the task within the DAG context
    run_ingest_batch = BashOperator(
        task_id="run_ingest_batch",
        bash_command = f"echo Hello World",
        dag=dag
    )
    
    # Define the task within the DAG context
    run_validatedb_batch = BashOperator(
        task_id="run_validatedb_batch",
        bash_command = f"python3 {SRC_PATH / 'pretest.py'}",
        dag=dag
    )
    
    # Data Pipeline
    run_prevalidate_batch >> run_transform_batch >> run_ingest_batch >> run_validatedb_batch
    
    
# If test turn-on individual data pipeline
if CONFIG.TEST:
    with DAG(
        "00-PreValidateData",
        default_args=CONFIG.DEFAULT_ARGS,
        schedule_interval=None,
        catchup=False
        ) as dag:
        
        # Define the task within the DAG context
        run_prevalidate = BashOperator(
            task_id="run_prevalidate",
            bash_command = f"python3 {SRC_PATH / 'pretest.py'}",
            dag=dag
        )
    
    
    with DAG(
        "01-TransformData",
        default_args=CONFIG.DEFAULT_ARGS,
        schedule_interval=None,
        catchup=False
        ) as dag:
        
        # Define the task within the DAG context
        run_transform = BashOperator(
            task_id="run_transform",
            bash_command = f"python3 {SRC_PATH / 'transform.py'}",
            dag=dag
        )
        
    with DAG(
        "02-IngestData",
        default_args=CONFIG.DEFAULT_ARGS,
        schedule_interval=None,
        catchup=False
        ) as dag:
        
        # Define the task within the DAG context
        run_ingest = BashOperator(
            task_id="run_ingest",
            bash_command = f"python3 {SRC_PATH / 'ingest.py'}",
            dag=dag
        )
        
    with DAG(
        "03-ValidateDBData",
        default_args=CONFIG.DEFAULT_ARGS,
        schedule_interval=None,
        catchup=False
        ) as dag:
        
        # Define the task within the DAG context
        run_validate_db = BashOperator(
            task_id="run_validate_db",
            bash_command = f"python3 {SRC_PATH / 'validate_ingest.py'}",
            dag=dag
        )

    # with DAG(
    #     "99-DeleteDBData",
    #     default_args=CONFIG.DEFAULT_ARGS,
    #     schedule_interval=None,
    #     catchup=False
    #     ) as dag:
        
    #     # Define the task within the DAG context
    #     run_cleaning = BashOperator(
    #         task_id="run_extraction",
    #         bash_command = f"echo Hello World",
    #         dag=dag
    #     )
        
if __name__ == "__main__":
    None