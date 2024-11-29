from snowflake.snowpark import Session
session = Session.builder.config("connection_name", "aoc_connection").create()

print(session.sql('select current_user()').collect())