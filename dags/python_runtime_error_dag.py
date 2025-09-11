from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Fix for ZeroDivisionError in python_runtime_error_dag
def cause_a_division_by_zero_error():
    # Fixed: Changed division by zero to a valid division
    result = 1 / 1
    print(f"Result of division: {result}")

with DAG(
    dag_id='python_runtime_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    division_by_zero_task = PythonOperator(
        task_id='division_by_zero_task',
        python_callable=cause_a_division_by_zero_error,
    )