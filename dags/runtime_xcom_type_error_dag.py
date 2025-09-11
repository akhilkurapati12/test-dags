from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _push_xcom_value(**kwargs):
    kwargs['ti'].xcom_push(key='my_int_value', value=123)

def _pull_and_fail_task_callable(**kwargs):
    ti = kwargs['ti']
    int_value = ti.xcom_pull(key='my_int_value', task_ids='push_xcom_task')
    # Ensure proper type casting to string before concatenation
    result = "The value is: " + str(int_value)
    print(result)

with DAG(
    dag_id='runtime_xcom_type_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    push_xcom_task = PythonOperator(
        task_id='push_xcom_task',
        python_callable=_push_xcom_value,
    )

    pull_and_fail_task = PythonOperator(
        task_id='pull_and_fail_task',
        python_callable=_pull_and_fail_task_callable,
    )

    push_xcom_task >> pull_and_fail_task
