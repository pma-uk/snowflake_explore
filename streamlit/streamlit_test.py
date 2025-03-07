import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get current credentials
session = get_active_session()

# Title and description
st.title("Streamlit in Snowflake Test")

# Set up columns for buttons
button_cols = st.columns(2)

# Show Customers
if button_cols[0].button("Show Customers"):
    rows = session.sql("SELECT * FROM CUSTOMERS;").collect()
    st.write(rows)

# Show Products
if button_cols[1].button("Show Products"):
    rows = session.sql("SELECT * FROM PRODUCTS;").collect()
    st.write(rows)