from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _failing_python_task_callable():
    # Define the missing variable 'my_undefined_data_path'
    my_undefined_data_path = "/tmp/data" # Example initialization
    print(f"Data path: {my_undefined_data_path}")

with DAG(
    dag_id='runtime_name_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    failing_python_task = PythonOperator(
        task_id='failing_python_task',
        python_callable=_failing_python_task_callable,
    )
