import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "getting-started"],
    doc_md="""
    ### Hello World DAG

    A simple DAG to demonstrate basic task dependency and execution in Composer 2.
    - `print_hello`: Prints 'Hello'.
    - `print_world`: Prints 'World!'. This task depends on the successful completion of `print_hello`.
    """,
) as dag:
    # Task to print "Hello"
    print_hello = BashOperator(
        task_id="print_hello",
        bash_command="echo 'Hello'",
    )

    # Task to print "World!"
    print_world = BashOperator(
        task_id="print_world",
        bash_command="echo 'World!'",
    )

    # Set the dependency: print_hello must run before print_world
    print_hello >> print_world