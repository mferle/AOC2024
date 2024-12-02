from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC02_example.txt", "@aoc_files_stage", auto_compress=False)
#session.file.put("AOC02_input.txt", "@aoc_files_stage", auto_compress=False)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC02", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC02_part1_part2.py'])
def AOC02(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, StringType
    from AOC02_part1_part2 import Part1Part2
    import logging

    logger = logging.getLogger("snowpark_logger")
    logger.info("Start Advent of Code Day 2")

    schema_for_csv = StructType([
                          StructField("REPORTS", StringType())
                       ])

    df = session.read.schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}").collect()
    logger.info(f"File {file_name} successfully read")

    report_lines = [l.asDict()["REPORTS"] for l in df]
    reports = [r.split(' ') for r in report_lines]

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(reports, logger)

    logger.info("Start Part 1")
    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    logger.info("Start Part 2")
    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return_msg = f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}"
    logger.info(f"End Advent of Code Day 2: {return_msg}")
    return return_msg

lines_df = session.sql("""call AOC02('AOC02_example.txt')""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC02(session, 'AOC02_example.txt'))

session.close()