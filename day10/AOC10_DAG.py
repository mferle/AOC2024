from snowflake.snowpark import Session
from snowflake.core import Root
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation
from snowflake.core.task import Cron

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# create the root object
root = Root(session)

with DAG("AOC2024_DAG", schedule=Cron("0 6 * * *", "UTC"), warehouse="AOC_WH") as dag:
    AOC08_task = DAGTask(name="AOC08_task", 
                  definition="call AOC08(build_scoped_file_url(@aoc_files_stage, 'AOC08_input.txt'))",
                  warehouse="AOC_WH")
    AOC09_task = DAGTask(name="AOC09_task", 
                  definition="call AOC09(build_scoped_file_url(@aoc_files_stage, 'AOC09_input.txt'))",
                  warehouse="AOC_WH")
    AOC10_task = DAGTask(name="AOC10_task", 
                  definition="call AOC10(build_scoped_file_url(@aoc_files_stage, 'AOC10_input.txt'))",
                  warehouse="AOC_WH")

# define the dependencies
AOC08_task >> [AOC09_task, AOC10_task]

# deploy the DAG
dag_op = DAGOperation(root.databases["AOC2024_DB"].schemas["AOC"])
dag_op.deploy(dag)
