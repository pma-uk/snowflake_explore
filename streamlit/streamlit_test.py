import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get current credentials
session = get_active_session()

# Title and description
st.title("Streamlit in Snowflake Test")


# Set up columns for buttons
button_cols = st.columns([1,1,1,1]) # Array specifies relative width of columns (brings buttons closer together)

# Set stage to track what should be displayed
# 0 - None; 1 - Customers; 2 - Orders; 3 - Products
if 'stage' not in st.session_state:
    st.session_state.stage = 0


# Show Customers
if button_cols[0].button("Show Customers"):
    st.session_state.stage = 1

# Show Orders
if button_cols[1].button("Show Orders"):
    st.session_state.stage = 2


# Check the stage and display it correspondingly
# Customers
if st.session_state.stage == 1:
    rows = session.sql("SELECT * FROM CUSTOMERS;").collect()
    st.write(rows)

# Orders
if st.session_state.stage == 2:
    query = """
    SELECT O.ORDER_ID, C.NAME AS CUSTOMER, P.NAME AS PRODUCT, O.QUANTITY, O.TOTAL_PRICE, O.ORDER_DATE
    FROM ORDERS O
    JOIN CUSTOMERS C ON C.ID = O.CUSTOMER_ID
    JOIN PRODUCTS P ON P.PRODUCT_ID = O.PRODUCT_ID
    ORDER BY O.ORDER_DATE DESC;
    """
    rows = session.sql(query).collect()
    st.write(rows)
