import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

with DAG(
    dag_id="runtime_sensor_timeout_dag",
    start_date=pendulum.datetime(2025, 9, 13, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["team-a", "test"],
) as dag:
    wait_for_nonexistent_file = GCSObjectExistenceSensor(
        task_id="wait_for_nonexistent_file",
        bucket="tmaf-test-dags-bucket",
        object="sample/file_that_will_never_exist.txt",
        poke_interval=10,
        timeout=120,  # Increased timeout from 60 to 120
    )

    task_that_will_be_skipped = BashOperator(
        task_id="task_that_will_be_skipped",
        bash_command="echo 'I will never run because the sensor failed.'",
    )

    wait_for_nonexistent_file >> task_that_will_be_skipped