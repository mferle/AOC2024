from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC01_example.txt", "@aoc_files_stage", auto_compress=False)
#session.file.put("AOC01_input.txt", "@aoc_files_stage", auto_compress=False)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC01", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC01_part1_part2.py'])
def AOC01(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, IntegerType
    from AOC01_part1_part2 import Part1Part2

    schema_for_csv = StructType([
                          StructField("LOC1", IntegerType()),
                          StructField("LOC2", IntegerType())
                       ])

    df = session.read.option("field_delimiter", "   ") \
        .schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}").collect()

    list1 = [l.asDict()["LOC1"] for l in df]
    list2 = [l.asDict()["LOC2"] for l in df]

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(list1, list2)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    return(f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}")

lines_df = session.sql("""call AOC01('AOC01_input.txt')""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC01(session, 'AOC01_example.txt'))

session.close()