import pendulum
import logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

def process_data():
    """
    This function attempts to use a variable that doesn't exist,
    which will cause a NameError at runtime.
    """
    logging.info("Starting the data processing task.")
    # Imagine this variable was supposed to be passed in or defined earlier.
    # Because it's not defined, this line will fail.
    # FIX: Define the variable my_undefined_data_path. 
    # Please update this path to the correct location of your data.
    my_undefined_data_path = "/path/to/your/data"
    data_path = my_undefined_data_path + "/source.csv"
    logging.info(f"This will never be logged. Path was: {data_path}")

with DAG(
    dag_id="runtime_name_error_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "runtime", "worker"],
) as dag:
    start_task = PythonOperator(
        task_id="start_task",
        python_callable=lambda: logging.info("DAG has started."),
    )

    failing_python_task = PythonOperator(
        task_id="failing_python_task",
        python_callable=process_data,
    )

    start_task >> failing_python_task