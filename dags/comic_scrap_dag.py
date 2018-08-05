from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator

from comic_dm5 import scrap_dm5


default_args = {
    'owner': 'bangyuwen',
    'depends_on_past': False,
    'start_date': datetime(2018, 8, 4),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG('comic_scrap', schedule_interval='0 16 * * *', default_args=default_args) as dag:
    t1 = PythonOperator(task_id='scrap_dm5',
                        python_callable=scrap_dm5.run)
    t2 = FileToGoogleCloudStorageOperator(src='/tmp/scrap_dm5/{{ yesterday_ds_nodash }}.csv',
                                          dst='/scrap_dm5/{{ yesterday_ds_nodash }}.csv',
                                          bucket='scrap-comic', google_cloud_storage_conn_id='google_cloud_default',
                                          mime_type='text/plain',  task_id='upload_to_GCS')
    t1 >> t2
