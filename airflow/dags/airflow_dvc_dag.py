from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

def update_data():
    with open("/opt/airflow/dags/data.txt", "r") as f:
        data = f.readlines()
        
    data = int(data[-1])
    print(f"Data: {data}")
    data += 1
    
    with open("/opt/airflow/dags/data.txt", "a") as f:
        f.write(f"\n{data}")
        

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
        
        git_init_node = BashOperator(
            task_id='git_init',
            bash_command='git init',
            cwd='/opt/airflow/dags'
        )
        
        # dvc_init_node = BashOperator(
        #     task_id='dvc_init',
        #     bash_command='dvc init --no-scm -f',
        #     cwd='/opt/airflow/dags'
        # )

        dvc_update_node = BashOperator(
            task_id='dvc_add',
            bash_command='dvc add /opt/airflow/dags/data.txt',
            cwd='/opt/airflow/dags'
        )
        
        dvc_set_gdrive_node = BashOperator(
            task_id='dvc_set_gdrive',
            bash_command='pip install dvc_gdrive && dvc remote add --default drive gdrive://1afYXggAkYObxdjaxK1eXH2wJ_JKN4-Nw -f && dvc remote modify drive gdrive_acknowledge_abuse true',
            cwd='/opt/airflow/dags'
        )
        
        dvc_push_node = BashOperator(
            task_id='dvc_push',
            bash_command='dvc push',
            cwd="/opt/airflow/dags"
        )

        # update_data_node >> git_init_node >> dvc_init_node >> dvc_update_node
        update_data_node >> git_init_node >> dvc_update_node
        # update_data_node >> git_init_node >> dvc_update_node >> dvc_set_gdrive_node >> dvc_push_node