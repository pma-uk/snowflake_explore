import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get current credentials
session = get_active_session()

# Title and description
st.title("Streamlit in Snowflake Test")

# Show Customers
if st.button("Show Customers"):
    rows = session.sql("SELECT * FROM CUSTOMERS LIMIT 10;").collect()
    st.write(rows)