from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 7, 17),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def format_hello(**kwargs):
    return 'Hello from Python !! Current execution time is ' + kwargs['execution_date'].strftime('%Y-%m-%d')


with DAG('hello-world-dag', schedule_interval=timedelta(minutes=5), catchup=False, default_args=default_args) as dag:

    # Define the task that prints hello with the bash operator.
    t1 = BashOperator(
        task_id='hello_from_bash',
        bash_command='echo Hello world from Bash !!')

    # Define a task that does nothing.
    t2 = DummyOperator(task_id='noop')

    # Define the task that prints hello using Python code.
    t3 = PythonOperator(task_id='hello_from_python', python_callable=format_hello, provide_context=True)

    # Define the DAG structure.
    t1 >> t2 >> t3
