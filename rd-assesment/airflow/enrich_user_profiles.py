from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    "enrich_user_profiles",
    default_args=default_args,
    catchup=False,
) as dag:
    glue_enrichment_job = GlueJobOperator(
        task_id="silver_to_gold_enrich_profiles",
        job_name="enrich_user_profiles_job",
        script_location="s3://<DataLakeBucket>/scripts/enrich_user_profiles.py",
        region_name="us-east-1",
        iam_role_name="<GlueServiceRole>",
        script_args={"--BUCKET_NAME": "<DataLakeBucket>"},
        aws_conn_id="aws_default",
    )
