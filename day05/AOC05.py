from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC05_example.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)
#session.file.put("AOC05_input.txt", "@aoc_files_stage", auto_compress=False, overwrite=True)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC05", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC05_part1_part2.py'])
def AOC05(session: Session, fileurl: str) -> str:
    from snowflake.snowpark.files import SnowflakeFile
    from AOC05_part1_part2 import Part1Part2

    # open the file and read the contents into a list by splitting on CRLF
    with SnowflakeFile.open(fileurl) as f:
        lines = f.read().split("\r\n")

    # to test locally, comment the previous two lines and open the file directly 
    #with open(fileurl) as f:
    #    lines = f.read().split("\n")

    # initialize pair ordering rules list
    all_pairs = []
    # initialize pages list
    pages = []
    # loop through lines and append to the appropriate list
    for l in lines:
        if l.find("|") != -1:
            all_pairs.append(l)
        if l.find(",") != -1:
            pages.append(l.split(','))

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(all_pairs, pages)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return_msg = f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}"
    return return_msg

lines_df = session.sql("""call AOC05(build_scoped_file_url(@aoc_files_stage, 'AOC05_input.txt'))""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC05(session, 'AOC05_input.txt'))

session.close()