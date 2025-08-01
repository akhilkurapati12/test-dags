import pendulum
import logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

def use_a_missing_library():
    """
    This function will fail if the 'scikit-learn' library is not installed
    in the Composer environment.
    """
    logging.info("Attempting to import a library that is likely not installed...")
    # This line will raise a ModuleNotFoundError at runtime.
    from sklearn.model_selection import train_test_split
    logging.info("Successfully imported scikit-learn! This should not happen.")

with DAG(
    dag_id="runtime_module_not_found_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "runtime", "dependencies"],
) as dag:
    failing_import_task = PythonOperator(
        task_id="failing_import_task",
        python_callable=use_a_missing_library,
    )