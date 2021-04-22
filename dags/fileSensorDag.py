import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.hooks.filesystem import FSHook
from airflow.operators.python_operator import PythonOperator


"""
- The dag uses File sensor operation to sense the arrival of file in the location
- in out case we putting txt file in the Airflow folder 
- we have define connection in the airflow ftp and in the extra 
    - we have to define the path of the uploaded file 
    - {"path":"/home/jaanhunzai_512/AirflowHome"}
"""

default_args = {
    "owner":"Sahib",
    "email":"jaanhunzai.5@gmail.com",
    "start_date":days_ago(1),
    "retries":1,
    "retry_delay":timedelta(minutes=1),
    "catchup":False
}
dag = DAG(
    dag_id = "fileSensorDag",
    default_args=default_args,
    schedule_interval=None
)

def print_file_contect(**content):
    hook = FSHook ("my_local_file_connect") # defined connection in the aiflow connections
    path = os.path.join(hook.get_path(), "test.txt")

    with open(path, "r")  as fp:
        print(fp.read())

    os.remove(path)

with dag:
    sensing_task = FileSensor(
        task_id="sensing_task",
        filepath="test.txt",
        fs_conn_id="my_local_file_connect",# add personal connection id
        poke_interval=10,
        #dag = dag
    )
    read_file_content = PythonOperator(
        task_id= "read_file_content",
        python_callable=print_file_contect,
        provide_context=True,
        retries=10,
        retry_delay=timedelta(seconds=1),

    )


sensing_task >> read_file_content