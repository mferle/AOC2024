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