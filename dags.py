from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from dataor import update_data
        

with DAG(
        dag_id='DVC-DAG',
        start_date=datetime(2023, 12, 7),
        schedule_interval='@once', 
        catchup=False
    ) as dag:
        
        update_data_node = PythonOperator(
            task_id='scrape_data',
            python_callable=update_data
        )
        
        dvc_init_node = BashOperator(
            task_id='dvc_init',
            bash_command='dvc init',
        )

        dvc_update_node = BashOperator(
            task_id='dvc_add',
            bash_command='dvc add data.txt',
        )
        
        dvc_push_node = BashOperator(
            task_id='dvc_push',
            bash_command='dvc push',
        )

        update_data_node >> dvc_init_node >> dvc_update_node >> dvc_push_node