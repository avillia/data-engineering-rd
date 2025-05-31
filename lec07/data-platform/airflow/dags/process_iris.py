from datetime import datetime, timedelta
from os import getenv

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from dbt_operator import DbtOperator
from python_scripts.train_model import process_iris_data

ANALYTICS_DB = getenv("ANALYTICS_DB", "analytics")
PROJECT_DIR = getenv("AIRFLOW_HOME") + "/dags/dbt/my_dbt_project"
PROFILE = "my_dbt_project"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["your_email@example.com"],  # change to your email
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="process_iris",
    default_args=default_args,
    description="Run dbt transformations and train ML model on Iris dataset",
    schedule_interval="0 1 * * *",
    start_date=datetime(2025, 4, 22),
    end_date=datetime(2025, 4, 24),
    catchup=False,
    tags=["dbt", "ml"],
)

env_vars = {
    "ANALYTICS_DB": ANALYTICS_DB,
    "DBT_PROFILE": PROFILE,
}

dbt_vars = {
    "is_test": False,
    "data_date": "{{ ds }}",
}

perform_transformations = DbtOperator(
    task_id="dbt_run_preprocessing",
    command="run",
    profile=PROFILE,
    project_dir=PROJECT_DIR,
    models=["iris_transformed"],
    env_vars=env_vars,
    vars=dbt_vars,
    dag=dag,
)

train_model = PythonOperator(
    task_id="train_model",
    python_callable=process_iris_data,
    dag=dag,
)

notify_success = EmailOperator(
    task_id="notify_success",
    to="your_email@example.com",  # change to your email
    subject="Airflow Iris DAG Success",
    html_content="""
        <h3>The Iris dataset pipeline has completed successfully!</h3>
        <p>dbt transformations and model training are done.</p>
    """,
    dag=dag,
)

perform_transformations >> train_model >> notify_success
