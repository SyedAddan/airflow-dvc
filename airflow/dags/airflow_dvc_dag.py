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
        )
        
        dvc_init_node = BashOperator(
            task_id='dvc_init',
            bash_command='dvc init --no-scm',
        )

        dvc_update_node = BashOperator(
            task_id='dvc_add',
            bash_command='dvc add /opt/airflow/dags/data.txt',
        )
        
        # dvc_push_node = BashOperator(
        #     task_id='dvc_push',
        #     bash_command='dvc push',
        # )

        update_data_node >> git_init_node >> dvc_init_node >> dvc_update_node