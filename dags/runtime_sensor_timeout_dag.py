from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.base import AirflowSensorTimeout
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from datetime import datetime, timedelta

# Fix for AirflowSensorTimeout in runtime_sensor_timeout_dag
with DAG(
    dag_id='runtime_sensor_timeout_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    wait_for_nonexistent_file = GCSObjectExistenceSensor(
        task_id='wait_for_nonexistent_file',
        bucket='your-gcs-bucket', # Placeholder: replace with actual bucket
        object='nonexistent_file.txt', # Placeholder: replace with actual object
        timeout=300,  # Increased timeout from 60 to 300 seconds
        poke_interval=5,
    )