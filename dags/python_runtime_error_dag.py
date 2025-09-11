from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _division_by_zero_callable():
    numerator = 10
    denominator = 0
    # Add a conditional check to prevent division by zero
    if denominator != 0:
        result = numerator / denominator
        print(result)
    else:
        print("Error: Division by zero is not allowed.")

with DAG(
    dag_id='python_runtime_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    division_by_zero_task = PythonOperator(
        task_id='division_by_zero_task',
        python_callable=_division_by_zero_callable,
    )
