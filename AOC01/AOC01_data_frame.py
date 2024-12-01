from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the data files to the internal stage - only needed once, then comment
#session.file.put("AOC01_example.txt", "@aoc_files_stage", auto_compress=False)
#session.file.put("AOC01_input.txt", "@aoc_files_stage", auto_compress=False)

# register a permanent stored procedure
@sproc(is_permanent=True, 
       name="AOC01_p", 
       replace=True, 
       stage_location="@aoc_dev_stage", 
       packages=['snowflake-snowpark-python', 'pandas'])
def AOC01_p(session: Session, file_name: str) -> str:
    from snowflake.snowpark.types import StructType, StructField, IntegerType
    import pandas as pd

    schema_for_csv = StructType([
                          StructField("LOC1", IntegerType()),
                          StructField("LOC2", IntegerType())
                       ])

    # read the data file into a Pandas data frame
    df = session.read.option("field_delimiter", "   ") \
        .schema(schema_for_csv).csv(f"@aoc_files_stage/{file_name}")

    # --- Part 1 ---

    # convert data frame to Pandas data frame
    dfp = df.to_pandas()

    # sort each column individually
    loc1sorted = dfp["LOC1"].sort_values(ignore_index=True)
    loc2sorted = dfp["LOC2"].sort_values(ignore_index=True)

    # construct a new Pandas data frame from the sorted columns
    dfs = pd.DataFrame()
    dfs["LOC1"] = loc1sorted
    dfs["LOC2"] = loc2sorted

    # calculate the difference
    dfs['DIFF'] = abs(dfs["LOC1"] - dfs["LOC2"])

    # sum the differences
    part1_answer = dfs["DIFF"].sum()

    # --- Part 2 ---

    # count and group by
    dfg = df.group_by("LOC2").count()

    # join the original df with the grouped and summarized dfg, using inner join
    dfj = df.join(dfg, df.col("LOC1") == dfg.col("LOC2")).select(df.col("LOC1"), dfg.col("COUNT"))

    # multiply the columns and sum
    df_sum = dfj.select_expr("LOC1 * COUNT").agg("$1", "sum").collect()

    # extract the answer as the first value of the first column
    part2_answer = df_sum[0].asDict()["SUM($1)"]
    
    return(f"Part 1 answer = {part1_answer}\nPart 2 answer = {part2_answer}")

lines_df = session.sql("""call AOC01_p('AOC01_example.txt')""")
lines_df.show()

# to test locally, comment the previous two lines and the sproc decorator
#print(AOC01_p(session, 'AOC01_example.txt'))

session.close()