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
        sql='SELECT * FROM `your-project.your_dataset.your_table` LIMIT 100', # Replace with your actual SQL query
        use_legacy_sql=False,
        gcp_conn_id='google_cloud_default',  # Ensure this connection uses a service account with bigquery.jobs.create permission
        # If a specific service account key file is used in a connection, ensure it has the necessary IAM roles.
        # This fix assumes the underlying permission issue will be resolved by granting
        # bigquery.jobs.create to the service account used by 'google_cloud_default' or
        # by configuring a new connection with a service account that has the permission.
    )