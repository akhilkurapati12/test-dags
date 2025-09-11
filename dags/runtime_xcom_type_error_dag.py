from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Fix for TypeError in runtime_xcom_type_error_dag
def push_value(**kwargs):
    kwargs['ti'].xcom_push(key='my_xcom_value', value="50")

def pull_and_do_math(**kwargs):
    pulled_value = kwargs['ti'].xcom_pull(key='my_xcom_value')
    # Cast pulled_value to int before performing arithmetic operations
    result = int(pulled_value) + 100
    print(f"Result of calculation: {result}")

with DAG(
    dag_id='runtime_xcom_type_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_value,
        provide_context=True,
    )

    pull_and_fail_task = PythonOperator(
        task_id='pull_and_fail_task',
        python_callable=pull_and_do_math,
        provide_context=True,
    )
    push_task >> pull_and_fail_task