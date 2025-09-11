from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

with DAG(
    dag_id='runtime_sensor_timeout_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    # Original timeout was 60 seconds, increasing to 300 seconds (5 minutes)
    wait_for_nonexistent_file = FileSensor(
        task_id='wait_for_nonexistent_file',
        filepath='/path/to/nonexistent/file.txt', # Replace with actual file path if applicable
        fs_conn_id='fs_default', # Assuming 'fs_default' connection exists
        poke_interval=5,
        timeout=300,  # Increased timeout from 60 to 300 seconds
        mode='reschedule',
    )