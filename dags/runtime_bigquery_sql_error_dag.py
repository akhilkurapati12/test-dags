import pendulum

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

# IMPORTANT: Replace with your GCP project and an existing BigQuery dataset.
# The service account running this DAG needs the `bigquery.jobs.create` permission.
GCP_PROJECT_ID = "tmaf-dev"
BIGQUERY_DATASET = "curated_logs"

with DAG(
    dag_id="runtime_bigquery_sql_error_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "composer-v2", "error", "runtime", "gcp"],
) as dag:
    # This query will fail if the service account does not have the necessary permissions.
    failing_sql_query = BigQueryInsertJobOperator(
        task_id="failing_sql_query_task",
        configuration={
            "query": {
                "query": f"SELECT 1 AS value FROM `{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.logs` LIMIT 1;",
                "useLegacySql": False,
                "destinationTable": {
                    "projectId": GCP_PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": "my_temp_output_table_{{ ds_nodash }}",
                },
                "createDisposition": "CREATE_IF_NEEDED",
                "writeDisposition": "WRITE_TRUNCATE",
            }
        },
    )