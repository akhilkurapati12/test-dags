import pendulum
import logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

def cause_a_division_by_zero_error():
    """
    This function will no longer fail with a ZeroDivisionError.
    """
    logging.info("This task will now succeed!")
    # FIX: Changed the divisor to a non-zero value.
    result = 1 / 1
    logging.info(f"This line will now be reached. Result was {result}")

with DAG(
    dag_id="python_runtime_error_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "debugging"],
    doc_md="A DAG that intentionally fails at runtime to demonstrate debugging.",
) as dag:
    failing_task = PythonOperator(
        task_id="division_by_zero_task",
        python_callable=cause_a_division_by_zero_error,
    )