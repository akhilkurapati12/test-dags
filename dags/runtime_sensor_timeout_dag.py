from airflow import DAG
from airflow.sensors.python import PythonSensor
from datetime import datetime, timedelta

def _check_condition():
    # Simulate a condition that might take longer than 60 seconds
    import time
    time.sleep(65)
    return True

with DAG(
    dag_id='runtime_sensor_timeout_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    wait_for_nonexistent_file = PythonSensor(
        task_id='wait_for_nonexistent_file',
        python_callable=_check_condition,
        timeout=300, # Increased timeout to 300 seconds
        poke_interval=5,
        mode='poke',
    )
