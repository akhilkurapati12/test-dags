import pendulum
from datetime import timedelta

from airflow.models.dag import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.operators.bash import BashOperator

# IMPORTANT: Use a real GCS bucket you have access to.
GCS_BUCKET = "tmaf-test-dags-bucket"

with DAG(
    dag_id="runtime_sensor_timeout_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "runtime", "sensor"],
) as dag:
    # This sensor will poke GCS every 10 seconds for a file that we will never create.
    # It will time out after 60 seconds.
    wait_for_nonexistent_file = GCSObjectExistenceSensor(
        task_id="wait_for_nonexistent_file",
        bucket=GCS_BUCKET,
        object="sample/file_that_will_never_exist.txt",
        mode="poke", # 'poke' mode keeps the worker slot busy
        poke_interval=10,
        timeout=300, # Fail the task after 300 seconds (5 minutes) of waiting
    )

    task_that_will_be_skipped = BashOperator(
        task_id="task_that_will_be_skipped",
        bash_command="echo 'I will never run because the sensor failed.'",
    )

    wait_for_nonexistent_file >> task_that_will_be_skipped