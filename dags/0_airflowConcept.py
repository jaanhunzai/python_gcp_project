from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "sahib",
    "email":"jaanhunzai.5@gmail.com",
    "start_date":datetime(2017, 3, 20),
    "retries":1,
    "retry_delay":timedelta(minutes=5),
     "catchup":False
}

templated_command = """
{% for i in range(5} %}
    echo "{{ ds }}"
    echo "{{ macro.ds_add (ds, 7 )}}"
    echo "{{ param.my_param}}"
{% endfor %} 
"""

with DAG(
    "airflowConcepts",
    default_args=default_args,
    schedule_interval = "@daily"
) as dag:


    task1 = BashOperator(
        task_id= "task1",
        bash_command='date',
    )

    task2 = BashOperator(
        task_id="task2",
        depends_on_past=False,
        bash_command='sleep 5',

    )

    task3 = BashOperator(
        task_id="task3",
        depends_on_past=False,
        bash_command=templated_command,
        params={"my_param":'here you go '},

    )
    task1 >> [task2,task3]