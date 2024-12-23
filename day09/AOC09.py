from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
session.file.put("AOC09_example.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)
session.file.put("AOC09_input.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC09", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC09_part1_part2.py'])
def AOC09(session: Session, fileurl: str) -> str:
    from snowflake.snowpark.files import SnowflakeFile
    from AOC09_part1_part2 import Part1Part2

    # open the file and read the contents into a list by splitting on CRLF
    with SnowflakeFile.open(fileurl) as f:
        lines = f.read().split("\r\n")

    # to test locally, comment the previous two lines and open the file directly 
    #with open(fileurl) as f:
    #    lines = f.read().split("\n")

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(lines[0])

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return_msg = f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}"
    return return_msg

lines_df = session.sql("""call AOC09(build_scoped_file_url(@aoc_files_stage, 'AOC09_example.txt'))""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC09(session, 'AOC09_example.txt'))

session.close()