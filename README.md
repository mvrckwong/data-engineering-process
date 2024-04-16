# Data Engineer Solutions
<a name="readme-top"></a>
All outputs are within ".output" folder. The project implements the following:
- End-to-End data processes. Similar to ETL data process.
- Streamlit Application to visualize the user data.
- Docker and Poetry to manage the project dependencies.
- Airflow to manage the data pipeline.
- Data processes, such as pretest.py, transform.py, ingest.py and validate_ingest.py to validate, transform and ingest the data.

*Note: Database credentials are already revoked.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Process Diagram
![Diagram](/.output/diagram.png)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Thought Process / Methodology
- If the data is to be ingested periodically, what changes will you make to your current approach? *We can easily make changes in the data pipeline or airflow dags. We can manage a specific tasks inside airflow dashboard, particularly ingestion of data to the database.*
- How will you verify the correctness of the ingested data? *As defined in the project, we will be using the command line with poetry to run the validate_ingest.py. The function will validate if the transformation done locally is transferred to the database. At the same time, we implemented pretest.py to validate the correctness of the data. We can test the correctness before intesting it to the database. Those implemented are unique per data table and column. This can be scaled further with great-expectations library.*
- *Reproducibility is key in managing large scale data-pipelines. Here we separated implementation of dags and src code. This is to make it easier to reproduce and test the code further.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Data Processes
There are 4 python data processes implemented. 

- Pretest.py - Implemented ensure correctness. For example, checking the primary key and foreign key for null and blanks. Checking for negative values to non-negative values. 
- Transform.py - Transform and clean the data, before ingesting it to the database. This includes: transforming the data, data type, data format, and data cleaning, checking for null, blanks, and invalid values.
- Ingest.py - Ingest the data to the database.
- Validate_Ingest.py - Monitor the ingested data, compared with the local.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started (Implementation)
 The data pipeline is responsible for loading the data and processing it. The streamlit application is responsible for displaying the data and providing the user with an interactive interface. Therefore, the data pipeline and the streamlit application are separated in the deployment.


### Prerequisite

Before running the python streamlit application, you should have the following installed in your local machine. 

1. Install the Python 3.9 or higher version, until 3.11. Also, install the latest version of the docker. We will be using docker-compose to run the airflow application (future) and the streamlit application.
2. Install the poetry library. The library will handle all your python dependencies and virtual environment in your local machine.
    ``` bash
    pip install poetry
    ```
3. Install the project dependencies by installing. Poetry will handle all your python dependencies and virtual environment in your local machine.
    ``` bash
    poetry install
    ```

### Running the Data Pipeline

Right now, some python functions are not 100% working in Airflow Deployment. For now, we will be using the command line with poetry to run the data-pipeline.

- Running the pretest.py
    ``` bash
    poetry run python src/pretest.py
    ```
- Running the transform.py
    ``` bash
    poetry run python src/transform.py
    ```
- Running the ingest.py
    ``` bash
    poetry run python src/ingest.py
    ```
- Running the validate_ingest.py
    ``` bash
    poetry run python src/validate_ingest.py
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Airflow Application (Future Developments)
To run the airflow application, you can run the following command. Airflow is important for data engineering because it provides a robust, scalable platform to programmatically author, schedule, and monitor workflows. 
```bash
docker-compose -f docker-compose.airflow.yml up
```
![AirflowDashboard](/.output/airflow-dashboard.png)

*Note: the data pipeline inside airflow is not yet functional. Two functions are already working - transform.py and pretest.py. Interaction with the database is not yet functional, because of dependencies issues.*

![AirflowPipeline](/.output/airflow-pipeline.png)
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Streamlit Application (Working)

To run the streamlit application, you can run the following command.
```bash
docker-compose -f docker-compose.app.yml up
```

Once the streamlit application is running, you'll be greeted with an intuitive user interface. Here's how you can get the most out of your data visualization experience. Enter a user name and click submit, you will be able to see the graph and the data for that user.

![streamlit](/.output/streamlit-app.png)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

