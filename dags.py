from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator

default_args = {
        'owner' : 'airflow',
        'start_date' : datetime(2022, 11, 12)
        }

dag = DAG(
        dag_id='DAG-1',
        default_args=default_args, 
        catchup=False
    )

start = EmptyOperator(task_id='start', dag=dag)

end = EmptyOperator(task_id='end', dag=dag)

start >> end