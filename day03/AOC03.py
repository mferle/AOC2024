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
       name="AOC03", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC03_part1_part2.py'])
def AOC03(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, StringType
    from AOC03_part1_part2 import Part1Part2

    schema_for_csv = StructType([
                          StructField("PROGRAM", StringType())
                       ])

    session.sql("create file format if not exists aoc03_csv_format type = csv, field_delimiter = NONE").collect()
    df = session.read.option("format_name", "aoc03_csv_format").schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}").collect()

    program = ''
    for l in df:
        program = program + l.asDict()["PROGRAM"]
    #print(program)

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(program)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return_msg = f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}"
    return return_msg

lines_df = session.sql("""call AOC03('AOC03_example.txt')""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC03(session, 'AOC03_example2.txt'))

session.close()