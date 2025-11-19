from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_world():
    print("Hello from example DAG")


def create_dag():
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(
        dag_id='example_hello_world',
        default_args=default_args,
        start_date=datetime(2023, 1, 1),
        schedule_interval='@daily',
        catchup=False,
    )

    with dag:
        t1 = PythonOperator(
            task_id='hello_task',
            python_callable=hello_world,
        )

    return dag

# Instantiate the DAG
globals()['example_hello_world'] = create_dag()
