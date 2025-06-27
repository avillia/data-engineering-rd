from datetime import datetime

from airflow import DAG
from airflow.providers.amazon.aws.hooks.glue_crawler import GlueCrawlerHook
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.standard.operators.python import PythonOperator


def start_glue_crawler(crawler_name):
    hook = GlueCrawlerHook(region_name="eu-central-1")
    hook.start_crawler(crawler_name)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
}

MIDNIGHT_DAILY = "0 0 * * *"

with DAG(
    "process_sales",
    default_args=default_args,
    schedule=MIDNIGHT_DAILY,
    catchup=False,
) as dag:
    run_crawler = PythonOperator(
        task_id="run_sales_crawler",
        python_callable=start_glue_crawler,
        op_kwargs={"crawler_name": "sales_bronze_crawler"},
    )

    glue_etl_job = GlueJobOperator(
        task_id="bronze_to_silver",
        job_name="sales_bronze_to_silver",
        script_location="s3://<DataLakeBucket>/scripts/glue_sales_etl.py",
        region_name="us-east-1",
        iam_role_name="<GlueServiceRole>",
        script_args={"--BUCKET_NAME": "<DataLakeBucket>"},
        aws_conn_id="aws_default",
    )

    run_crawler >> glue_etl_job
