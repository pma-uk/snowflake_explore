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

# Show Products
if button_cols[2].button("Show Products"):
    st.session_state.stage = 3


# Check the stage and display it correspondingly
# Customers
if st.session_state.stage == 1:
    rows = session.sql("SELECT * FROM CUSTOMERS;").collect()
    st.write(rows)

    cust_left, cust_right = st.columns([2,1])
    
    # Form for adding new customer
    with cust_left.form("add_customer"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        submitted = st.form_submit_button("Add Customer")

        if submitted:
            session.sql("""
                        INSERT INTO CUSTOMERS (NAME, EMAIL, ADDRESS)
                        VALUES (?, ?, ?)
                        """, 
                        params=[name, email, address]).collect()
            
            st.success("Customer added!")
            st.rerun()

    # For deleting customer
    with cust_right.form("del_customer"):
        cust_id = st.text_input("Customer ID")
        if st.form_submit_button("Delete Customer"):
            session.sql("""
                        DELETE FROM CUSTOMERS
                        WHERE ID = ?
                        """,
                       params=[cust_id]).collect()
            session.sql("""
                        DELETE FROM ORDERS
                        WHERE CUSTOMER_ID = ?
                        """,
                       params=[cust_id]).collect()
            st.success(f"Deleted customer with ID {cust_id}")
            st.rerun()

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

# Products
if st.session_state.stage == 3:
    rows = session.sql("SELECT * FROM PRODUCTS;").collect()
    st.write(rows)

    prod_left, prod_right = st.columns([2,1])

    with prod_left.form("add_product"):
        name = st.text_input("Name")
        category = st.text_input("Category")
        price = st.number_input("Price")
        submitted = st.form_submit_button("Add Product")

        if submitted:
            session.sql("""
                        INSERT INTO PRODUCTS (NAME, CATEGORY, PRICE)
                        VALUES (?, ?, ?)
                        """, 
                        params=[name, category, price]).collect()
            
            st.success("Product added!")
            st.rerun()

    with prod_right.form("del_product"):
        prod_id = st.text_input("Product ID")
        if st.form_submit_button("Delete Product"):
            session.sql("""
                        DELETE FROM PRODUCTS
                        WHERE PRODUCT_ID = ?
                        """,
                       params=[prod_id]).collect()
            session.sql("""
                        DELETE FROM ORDERS
                        WHERE PRODUCT_ID = ?
                        """,
                       params=[prod_id]).collect()
            st.success(f"Deleted product with ID {prod_id}")
            st.rerun()
