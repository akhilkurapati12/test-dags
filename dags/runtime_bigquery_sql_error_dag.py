from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from datetime import datetime

with DAG(
    dag_id='runtime_bigquery_sql_error_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    failing_sql_query_task = BigQueryExecuteQueryOperator(
        task_id='failing_sql_query_task',
        sql="SELECT 1 FROM non_existent_table",
        use_legacy_sql=False,
        gcp_conn_id='google_cloud_default',
    )
# Recommendation: The service account running this task needs 'bigquery.jobs.create' permission.
# This is an IAM configuration change and cannot be fixed directly in the code.
# Please ensure the service account associated with 'google_cloud_default' connection has the necessary permissions.
