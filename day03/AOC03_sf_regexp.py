from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC03_example.txt", "@aoc_files_stage", auto_compress=False)
#session.file.put("AOC03_example2.txt", "@aoc_files_stage", auto_compress=False)
#session.file.put("AOC03_input.txt", "@aoc_files_stage", auto_compress=False)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC03_s", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'])
def AOC03_s(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, StringType

    schema_for_csv = StructType([
                          StructField("PROGRAM", StringType())
                       ])

    # create a file format specifying the delimiter is NONE
    session.sql("create file format if not exists aoc03_csv_format type = csv, field_delimiter = NONE").collect()
    # read the file into a data frame using the file format
    df = session.read.option("format_name", "aoc03_csv_format").schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}")

    # save the data frame as a Snowflake table
    df.write.mode("overwrite").save_as_table("day03_program")

    # define the regexp pattern as a raw string literal because it contains backslashes
    regexp_pattern = r"^\\d*,\\d*\\)"

    # use SQL to calculate the result
    part1_answer_df = session.sql(f"""
        with program_parts as (
            select split(program, 'mul(') as program_parts 
            from day03_program
        ),
        program_value as (
            select program_part.value::varchar as program_value 
            from program_parts, 
            lateral flatten(input => program_parts) AS program_part
        ),
        program_substr as (
            select replace(regexp_substr(program_value, '{regexp_pattern}'), ')', '') as program_substr 
            from program_value 
            where regexp_like(program_value, '{regexp_pattern}.*')
        ),
        program_multiply as (
            select split_part(program_substr, ',', 1)::integer * split_part(program_substr, ',', 2)::integer as program_multiply 
            from program_substr
        )
        select sum(program_multiply) as part1_answer 
        from program_multiply
        """).collect()

    part1_answer = part1_answer_df[0].asDict()["PART1_ANSWER"]

    return_msg = f"Part 1 answer = {part1_answer}"
    return return_msg

lines_df = session.sql("""call AOC03_s('AOC03_example.txt')""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC03_s(session, 'AOC03_example.txt'))

session.close()