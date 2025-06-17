from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'aditya',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xpenz_etl_dag',
    default_args=default_args,
    description='Run my main Python script using Airflow',
    schedule_interval='0 0 * * *',  # or '0 10 * * *' for 10 AM daily
    start_date=datetime(2025, 6, 15),
    catchup=False,
)

run_script = BashOperator(
    task_id='xpenz_etl',
    bash_command='python3 /mnt/d/App/repository/xpenz/main.py',
    dag=dag,
)