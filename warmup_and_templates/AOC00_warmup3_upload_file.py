from snowflake.snowpark import Session

# establish the session with Snowflake
session = Session.builder.config("connection_name", "aoc_connection").create()

# upload the file with example data to the aoc_files_stage stage
session.file.put("warmup1_example.txt", "@aoc_files_stage", auto_compress=False)
session.file.put("warmup1_input.txt", "@aoc_files_stage", auto_compress=False)

session.close()