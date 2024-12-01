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
grant usage on database aoc2024_db to role aoc_developer;
grant all on schema aoc to role aoc_developer;
grant usage on warehouse aoc_wh to role aoc_developer;

-- create an internal stage for data files
create or replace stage aoc_files_stage;

-- create an internal stage for Python code
create or replace stage aoc_dev_stage;
