from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC14_example.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)
#session.file.put("AOC14_input.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC14_p", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC14_part1_part2.py'])
def AOC14_p(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, StringType

    schema_for_csv = StructType([
                          StructField("POSITION", StringType()),
                          StructField("VELOCITY", StringType())
                       ])

    df = session.read.option("field_delimiter", " ") \
        .schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}")

    # save the data frame as a Snowflake table
    df.write.mode("overwrite").save_as_table("day14_robots")

    return 'Success'

lines_df = session.sql("""call AOC14_p('AOC14_input.txt')""")
lines_df.show()

session.close()

# Perform the following statements in a Snowflake worksheet
# parse the ingested data into the px, py, vx, and vy columns
"""
create or replace view day14_robots_v as
select 
  split_part(replace(position, 'p=', ''), ',', 1)::integer as px, 
  split_part(replace(position, 'p=', ''), ',', 2)::integer as py, 
  split_part(replace(velocity, 'v=', ''), ',', 1)::integer as vx,
  split_part(replace(velocity, 'v=', ''), ',', 2)::integer as vy
from day14_robots;
"""

# transform the data for visualization
"""
create or replace view day14_robots_final as
with newpxpy as (
  select (px + (7569 * vx)) % 101 as new_px, 
    (py + (7569 * vy)) % 103 as new_py
  from day14_robots_v
),
neg_mod as (
  select
    case when new_px < 0 then 101 + new_px else new_px end as px,
    case when new_py < 0 then 103 + new_py else new_py end as py
  from newpxpy
)
select px, 103-py-1 as py
from neg_mod;
"""
