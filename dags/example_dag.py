from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.sensors.python import PythonSensor

with DAG(
    dag_id="example_dag",
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:
    # [START example_python_sensor]
    PythonSensor(
        task_id="wait_for_condition",
        python_callable=lambda: True,  # Replace with your actual condition check
        timeout=60 * 10,  # Updated timeout to 10 minutes
        mode="poke",
    )
    # [END example_python_sensor]