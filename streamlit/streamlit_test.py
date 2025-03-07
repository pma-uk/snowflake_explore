import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get current credentials
session = get_active_session()

# Title and description
st.title("Streamlit in Snowflake Test")

# Set up columns for buttons
button_cols = st.columns([1,1,1]) # Array specifies relative width of columns (brings buttons closer together)

# Show Customers
if button_cols[0].button("Show Customers"):
    rows = session.sql("SELECT * FROM CUSTOMERS;").collect()
    st.write(rows)

# Show Orders
if button_cols[1].button("Show Orders"):
    query = """
    SELECT O.ORDER_ID, C.NAME AS CUSTOMER, P.NAME AS PRODUCT, O.QUANTITY, O.TOTAL_PRICE, O.ORDER_DATE
    FROM ORDERS O
    JOIN CUSTOMERS C ON C.ID = O.CUSTOMER_ID
    JOIN PRODUCTS P ON P.PRODUCT_ID = O.PRODUCT_ID
    ORDER BY O.ORDER_DATE DESC;
    """
    rows = session.sql(query).collect()
    st.write(rows)
