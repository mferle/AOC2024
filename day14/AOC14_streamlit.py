# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("Advent of Code Day 14")
st.write("Move robots until they form a Christmas tree")

# Get the current credentials
session = get_active_session()

# read the DAY14_ROBOTS_FINAL view into a data frame
df = session.sql("""
  select px, py 
  from AOC2024_DB.AOC.DAY14_ROBOTS_FINAL""")

# visualize the data in the data frame as a scatter plot
st.scatter_chart(df, x="PX", y="PY", color = "#09ab3b", size = 10)