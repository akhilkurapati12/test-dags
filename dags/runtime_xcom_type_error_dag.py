import pendulum
import logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

def push_a_string_value(**context):
    """
    Pushes a string value to XComs.
    """
    logging.info("Pushing the string '500' to XComs.")
    context["ti"].xcom_push(key="my_value", value="500")

def pull_and_do_math(**context):
    """
    Pulls the XCom value and tries to perform math with it.
    """
    pulled_value = context["ti"].xcom_pull(key="my_value", task_ids="push_task")
    logging.info(f"Pulled value '{pulled_value}' of type {type(pulled_value)} from XComs.")
    
    # Convert the pulled value to an integer before performing addition.
    result = int(pulled_value) + 100
    logging.info(f"The result was {result}")

with DAG(
    dag_id="runtime_xcom_type_error_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "runtime", "xcoms"],
) as dag:
    push_task = PythonOperator(
        task_id="push_task",
        python_callable=push_a_string_value,
    )

    pull_and_fail_task = PythonOperator(
        task_id="pull_and_fail_task",
        python_callable=pull_and_do_math,
    )

    push_task >> pull_and_fail_task