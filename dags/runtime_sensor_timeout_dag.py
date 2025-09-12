import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

with DAG(
    dag_id="runtime_sensor_timeout_dag",
    start_date=pendulum.datetime(2025, 9, 11, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["team_a", "test_dag"],
) as dag:
    wait_for_nonexistent_file = GCSObjectExistenceSensor(
        task_id="wait_for_nonexistent_file",
        bucket="tmaf-test-dags-bucket",
        object="sample/file_that_will_never_exist.txt",
        mode="poke",
        poke_interval=10,
        timeout=300,
    )

    task_that_will_be_skipped = BashOperator(
        task_id="task_that_will_be_skipped",
        bash_command="echo 'This task will be skipped.'",
    )

    wait_for_nonexistent_file >> task_that_will_be_skipped