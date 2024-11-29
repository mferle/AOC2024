from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# register a permanent UDF
@udf(is_permanent=True, name="warmup1", replace=True, stage_location="@aoc_dev_stage", packages=['snowflake-snowpark-python'])
def warmup1(fileurl: str) -> str:
    from snowflake.snowpark.files import SnowflakeFile
    
    # open the file and read the contents into a list by splitting on CRLF
    with SnowflakeFile.open(fileurl) as f:
        lines = f.read().split("\r\n")
    return(lines)

# execute the UDF by providing a scoped file URL to the file in the stage
lines_df = session.sql("""select warmup1(build_scoped_file_url(@aoc_files_stage, 'warmup1_example.txt')) as lines""")
lines_df.show()
