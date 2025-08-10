from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'aditya',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='xpenz_etl_bash_dag',
    default_args=default_args,
    description='Run xpenz pipeline using BashOperator',
    schedule='0 0 * * *',
    start_date=datetime(2025, 6, 14),
    catchup=False,
    tags=['xpenz'],
) as dag:

    run_task = BashOperator(
        task_id='xpenz_etl_main',
        bash_command='cd /mnt/d/App/repository/xpenz && /mnt/d/App/devenv_p3_11/bin/python3 main.py',
    )