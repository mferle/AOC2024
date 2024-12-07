from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC07_example.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)
#session.file.put("AOC07_input.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)

# register a permanent stored procedure

@sproc(is_permanent=True, 
       name="AOC07_ingest", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'])
def AOC07_ingest(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, IntegerType, StringType
    from snowflake.snowpark.column import METADATA_FILE_ROW_NUMBER

    schema_for_csv = StructType([
                          StructField("TEST_VALUE", IntegerType()),
                          StructField("OPERANDS", StringType())
                       ])

    # read the file into a data frame using the file format
    df = session.read.with_metadata(METADATA_FILE_ROW_NUMBER.as_("RN")).option("field_delimiter", ":").schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}")

    # save the data frame as a Snowflake table
    table_name = file_name.split('.')[0]
    df.write.mode("overwrite").save_as_table(table_name)

    return 'Success'

#lines_df = session.sql("""call AOC07_ingest('AOC07_example.txt')""")
#lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
print(AOC07_ingest(session, 'AOC07_example.txt'))

session.close()