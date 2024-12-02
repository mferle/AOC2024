from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="warmup3", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC00_part1_part2.py', 'warmup1_example.txt'])
def warmup3(session: Session, filename: str) -> str:
    from snowflake.snowpark.files import SnowflakeFile
    from AOC00_part1_part2 import Part1Part2
    import sys
  
    import_dir = sys._xoptions["snowflake_import_directory"]

    # open the file and read the contents into a list by splitting on CRLF
    #with SnowflakeFile.open(fileurl) as f:
    with open(import_dir + filename) as f:
        lines = f.read().split("\n")
    
    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(lines)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return(f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}")

lines_df = session.sql("""call warmup3('warmup1_example.txt')""")
lines_df.show()

session.close()