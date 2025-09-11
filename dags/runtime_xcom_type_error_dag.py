from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.taskinstance import TaskInstance

def push_value(**kwargs):
    # This task simulates pushing a string value to XCom
    kwargs['ti'].xcom_push(key='my_xcom_value', value='100')

def pull_and_do_math(**kwargs):
    ti: TaskInstance = kwargs['ti']
    pulled_value = ti.xcom_pull(task_ids='push_value_task', key='my_xcom_value')

    # Cast the pulled_value to an integer before performing addition
    # The original error was: TypeError: can only concatenate str (not "int") to str
    try:
        numeric_value = int(pulled_value)
        result = numeric_value + 100
        print(f"Result of calculation: {result}")
    except ValueError:
        print(f"Error: Could not convert '{pulled_value}' to an integer.")

with DAG(
    dag_id='runtime_xcom_type_error_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    push_value_task = PythonOperator(
        task_id='push_value_task',
        python_callable=push_value,
    )

    pull_and_fail_task = PythonOperator(
        task_id='pull_and_fail_task',
        python_callable=pull_and_do_math,
    )

    push_value_task >> pull_and_fail_task