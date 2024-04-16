from datetime import datetime, timedelta
from pendulum import timezone

# Airflow Configuration
TEST:bool = True
DEFAULT_ARGS = {
    "owner": "Maverick Wong",
    "depends_on_past": True,
    
    "email": ["mvrckwong@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    
    "start_date": datetime(2024, 1, 1, tzinfo=timezone("Asia/Singapore")),
    "end_date": None,
    
    "schedule_interval": None,
    "catchup": False
}

if __name__ == "__main__":
    None