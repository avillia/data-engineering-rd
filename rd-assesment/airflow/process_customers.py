from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.glue_crawler import GlueCrawlerHook
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator


def start_glue_crawler(crawler_name):
    hook = GlueCrawlerHook()
    hook.start_crawler(crawler_name)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
}

AT_2_AM_UTC_MIDNIGHT = "0 2 * * *"

with DAG(
    "process_customers",
    default_args=default_args,
    schedule=AT_2_AM_UTC_MIDNIGHT,
    catchup=False,
) as dag:
    run_crawler = PythonOperator(
        task_id="run_customers_crawler",
        python_callable=start_glue_crawler,
        op_kwargs={"crawler_name": "customers_bronze_crawler"},
    )

    glue_etl_job = GlueJobOperator(
        task_id="bronze_to_silver_customers",
        job_name="customers_bronze_to_silver",
        script_location="s3://<DataLakeBucket>/scripts/customers.py",
        region_name="us-east-1",
        iam_role_name="<GlueServiceRole>",
        script_args={"--BUCKET_NAME": "<DataLakeBucket>"},
        aws_conn_id="aws_default",
    )

    run_crawler >> glue_etl_job
