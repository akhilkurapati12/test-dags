import logging
import pendulum

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def print_execution_date(**context):
    """
    Prints the logical execution date of the DAG run.
    This demonstrates accessing context variables passed by Airflow.
    """
    logical_date = context["ds"]
    logging.info(f"This DAG run is for the logical date: {logical_date}")
    print(f"This will also appear in the logs: {logical_date}")


with DAG(
    dag_id="python_and_templating_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["example", "composer-v2", "python", "templating"],
    doc_md="""
    ### Python Operator and Templating DAG

    Demonstrates two key concepts:
    1.  **PythonOperator**: Executes a Python callable.
    2.  **Jinja Templating**: Uses the `{{ ds }}` macro to dynamically print the execution date.
    """,
) as dag:
    # Task using a Python callable
    python_task = PythonOperator(
        task_id="print_logical_date_from_python",
        python_callable=print_execution_date,
    )

    # Task using BashOperator to show templating directly in the command
    bash_task_with_template = BashOperator(
        task_id="print_logical_date_from_bash",
        bash_command="echo 'The logical date from Bash is {{ ds }}'",
    )

    python_task >> bash_task_with_template