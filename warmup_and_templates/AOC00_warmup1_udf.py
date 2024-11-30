from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# register a permanent UDF
@udf(is_permanent=True, name="warmup1", replace=True, stage_location="@aoc_dev_stage", packages=['snowflake-snowpark-python'])
def warmup1(fileurl: str) -> int:
    from snowflake.snowpark.files import SnowflakeFile
    
    # open the file and read the contents into a list by splitting on CRLF
    with SnowflakeFile.open(fileurl) as f:
        lines = f.read().split("\r\n")
    
    # initialize the result
    total = 0
    # read each line in the list
    for line in lines:
        # find the first character that is a digit
        for chr in line:
            # if the character is a digit, save it and break from the loop
            if chr.isnumeric():
                first_digit = int(chr)
                break

        # repeat from reverse, find the last character that is a digit
        line_reverse = line[::-1]
        for chr in line_reverse:
            # if the character is a digit, save it and break from the loop
            if chr.isnumeric():
                last_digit = int(chr)
                break

        # add to the total
        total += 10*first_digit + last_digit

    return(total)

lines_df = session.sql("""select warmup1(build_scoped_file_url(@aoc_files_stage, 'warmup1_example.txt')) as lines""")
lines_df.show()

session.close()