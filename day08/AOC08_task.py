from snowflake.snowpark import Session
from snowflake.core import Root
from snowflake.core.task import Task
from snowflake.core.task import Cron

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# create the root object
root = Root(session)

# create a task object
AOC08_task = Task(name="AOC08_task", 
                  definition="call AOC08(build_scoped_file_url(@aoc_files_stage, 'AOC08_input.txt'))", 
                  schedule=Cron("0 6 * * *", "UTC"),
                  warehouse="AOC_WH")
# create a task collections objects, specifying the database and schema
AOC_tasks = root.databases['AOC2024_DB'].schemas['AOC'].tasks
# create the task in Snowflake
AOC_tasks.create(AOC08_task)

# comment and uncomment the following lines as needed
AOC_tasks_resource = AOC_tasks['AOC08_task']
AOC_tasks_resource.resume()
AOC_tasks_resource.execute()
AOC_tasks_resource.suspend()