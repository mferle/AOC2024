from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc
import time

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC07_solve", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python'],
       imports=['AOC07_part1_part2.py'])
def AOC07_solve(session: Session, table_name: str, all_groups: int, group: int) -> int:
    from AOC07_part1_part2 import Part1Part2

    df = session.sql(f"""select test_value, operands 
                     from {table_name} where rn%{all_groups} = {group}""").collect()

    lines = [f'{l.asDict()["TEST_VALUE"]}:{l.asDict()["OPERANDS"]}' for l in df]

    # instantiate the Part1Part2 class
    _Part1Part2 = Part1Part2(lines)

    # call the part1() module to solve Part 1
    part1_answer = _Part1Part2.part1()

    # call the part2() module to solve Part 2
    part2_answer = _Part1Part2.part2()

    #return_msg = f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}"
    return part1_answer

start_time = time.time()

# submit 4 jobs asynchronously
async_job1 = session.sql("""call AOC07_solve('AOC07_input', 4, 0)""").collect_nowait()
async_job2 = session.sql("""call AOC07_solve('AOC07_input', 4, 1)""").collect_nowait()
async_job3 = session.sql("""call AOC07_solve('AOC07_input', 4, 2)""").collect_nowait()
async_job4 = session.sql("""call AOC07_solve('AOC07_input', 4, 3)""").collect_nowait()

# keep looping and checking until they are all done
count_done = 0
while True:
    if async_job1.is_done():
        count_done += 1
    if async_job2.is_done():
        count_done += 1
    if async_job3.is_done():
        count_done += 1
    if async_job4.is_done():
        count_done += 1

    if count_done < 4:
        print(f'{count_done} groups are done, waiting')
        # wait 2 seconds before checking again
        time.sleep(2)
        count_done = 0
    else:
        print('all groups are done')
        break

# collect the results
total = 0
total += async_job1.result()[0].asDict()["AOC07_SOLVE"]
total += async_job2.result()[0].asDict()["AOC07_SOLVE"]
total += async_job3.result()[0].asDict()["AOC07_SOLVE"]
total += async_job4.result()[0].asDict()["AOC07_SOLVE"]
print(total)
print("--- %s seconds ---" % (time.time() - start_time))

session.close()
