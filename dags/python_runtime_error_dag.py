from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def cause_a_division_by_zero_error():
    numerator = 10
    denominator = 0
    # Fix: Add a try-except block to handle ZeroDivisionError gracefully
    try:
        result = numerator / denominator
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Division by zero attempted. Handled gracefully.")
        result = None # Or some default/error value
    return result

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