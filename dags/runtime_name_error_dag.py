from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Fix for NameError in runtime_name_error_dag
def process_data():
    my_undefined_data_path = "/path/to/my/data"  # Variable defined
    data_path = my_undefined_data_path + "/source.csv"
    print(f"Processing data from: {data_path}")

with DAG(
    dag_id='runtime_name_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    failing_python_task = PythonOperator(
        task_id='failing_python_task',
        python_callable=process_data,
    )