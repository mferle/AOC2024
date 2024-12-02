from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="warmup4", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC00_part1_part2.py'])
def warmup4(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, StringType
    from AOC00_part1_part2 import Part1Part2
    
    schema_for_csv = StructType([
                          StructField("CALIBRATION", StringType())
                       ])

    df = session.read.schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}").collect()

    lines = [l.asDict()["CALIBRATION"] for l in df]

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(lines)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return(f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}")

lines_df = session.sql("call warmup4('warmup1_example.txt')")
lines_df.show()
