from airflow import DAG
from airflow.decorators import task, dag, task_group
from datetime import datetime, timedelta

from scripts.download_kaggle_data import download_kaggle_dataset
from scripts.upload_s3 import upload_to_s3
from scripts.load_to_rds import load_to_rds

default_args = {
    'owner': 'uygar',
    "retries": 2,
    "timeout": 300,
}


@dag(
    dag_id="etl_pipeline",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2025,1,1), 
    catchup=False,
    tags=["olist","aws"]
)

def etl_pipeline():

    @task
    def task_download_data():
        download_kaggle_dataset()
    
    @task
    def task_upload_data():
        upload_to_s3()
    
    @task
    def task_load_to_rds():
        load_to_rds()
    
    task_download_data() >> task_upload_data() >> task_load_to_rds()



etl_pipeline()
    








