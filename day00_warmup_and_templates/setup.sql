-- setup the Snowflake environment

-- create a role
use role useradmin;
create role aoc_developer;
grant role aoc_developer to user <username>;

-- create a database, a schema, and a virtual warehouse
use role sysadmin;
create database aoc2024_db;
create schema aoc;
create warehouse aoc_wh;

-- grant usage on the database, schema, and warehouse to the role
use role sysadmin;
grant all on database aoc2024_db to role aoc_developer;
grant all on schema aoc to role aoc_developer;
grant usage on warehouse aoc_wh to role aoc_developer;

-- create an internal stage for data files
use role aoc_developer;
create or replace stage aoc_files_stage;

-- create an internal stage for Python code
create or replace stage aoc_dev_stage;

-- grant the execute task privilege to the aoc_developer role using the accountadmin role
use role accountadmin;
grant execute task on account to role aoc_developer;
-- switch back to the aoc_developer role
use role aoc_developer;

-- create an internal stage for the shared Python code
create or replace stage aoc_util_stage;

