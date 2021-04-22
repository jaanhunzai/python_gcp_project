from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
#from airflow import MultiplyBy5Operator


# from airflow.operators import MultiplyBy5Operator

def print_hello():
    return 'Hello Wolrd'


with DAG(
        'hello_world',
        description='Hello world example',
        schedule_interval='0 12 * * *',
        start_date=datetime(2017, 3, 20),
        catchup=False
) as dag:

    dummy_operator = DummyOperator(
        task_id='dummy_task',
        retries=3
    )
    hello_operator = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello
    )

    dummy_operator >> hello_operator

