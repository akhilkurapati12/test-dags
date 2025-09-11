from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def cause_a_division_by_zero_error():
    numerator = 10
    denominator = 0

    # Add a check to prevent division by zero
    if denominator != 0:
        result = numerator / denominator
        print(f"Result: {result}")
    else:
        print("Error: Cannot divide by zero.")
        # Optionally, raise an AirflowException or return a specific value
        # to indicate task failure or handle the error gracefully.
        # For demonstration, just printing an error.

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