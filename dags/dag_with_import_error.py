import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# This DAG has a syntax error. The closing parenthesis for the DAG constructor is missing.
with DAG(
    dag_id="dag_with_import_error",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "import-error"],
) as dag:
    correct_task = BashOperator(
        task_id="this_will_never_run",
        bash_command="echo 'This task is part of a broken DAG.'",
    )