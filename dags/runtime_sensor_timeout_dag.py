from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

with DAG(
    dag_id='runtime_sensor_timeout_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    wait_for_nonexistent_file = ExternalTaskSensor(
        task_id='wait_for_nonexistent_file',
        external_dag_id='nonexistent_dag',
        external_task_id='nonexistent_task',
        timeout=300, # Increased timeout to prevent AirflowSensorTimeout
        poke_interval=10, # Increased poke_interval
        mode='poke',
    )