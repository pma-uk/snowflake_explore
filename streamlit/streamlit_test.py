import streamlit as st
from snowflake.snowpark.context import get_active_session


# Get current Snowflake session
session = get_active_session()


# Display Customers
def show_customers():
    st.write("### Customers List")
    rows = session.sql("SELECT * FROM CUSTOMERS;").collect()
    st.write(rows)

    # Layout for adding and deleting customers
    cust_left, cust_right = st.columns([2, 1])

    with cust_left.form("add_customer"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        submitted = st.form_submit_button("Add Customer")

        if submitted and name and email and address:
            session.sql("""
                        INSERT INTO CUSTOMERS (NAME, EMAIL, ADDRESS)
                        VALUES (?, ?, ?)
                        """, 
                        params=[name, email, address]).collect()
            
            st.success("Customer added!")
            st.rerun()

    with cust_right.form("del_customer"):
        cust_id = st.text_input("Customer ID")
        if st.form_submit_button("Delete Customer") and cust_id:
            session.sql("DELETE FROM CUSTOMERS WHERE ID = ?", params=[cust_id]).collect()
            session.sql("DELETE FROM ORDERS WHERE CUSTOMER_ID = ?", params=[cust_id]).collect()
            st.success(f"Deleted customer with ID {cust_id}")
            st.rerun()


# Display Orders
def show_orders():
    st.write("### Orders List")
    query = """
            SELECT O.ORDER_ID, C.NAME AS CUSTOMER, P.NAME AS PRODUCT, P.TICKER AS TICKER, P.EXCHANGE AS EXCHANGE, O.QUANTITY, O.TOTAL_PRICE, O.ORDER_DATE
            FROM ORDERS O
            JOIN CUSTOMERS C ON C.ID = O.CUSTOMER_ID
            JOIN PRODUCTS P ON P.PRODUCT_ID = O.PRODUCT_ID
            ORDER BY O.ORDER_ID;
            """
    rows = session.sql(query).collect()
    st.write(rows)


# Display Products
def show_products():
    st.write("### Products List")
    rows = session.sql("SELECT * FROM PRODUCTS;").collect()
    st.write(rows)

    # Layout for adding and deleting products
    prod_left, prod_right = st.columns([2, 1])

    with prod_left.form("add_product"):
        name = st.text_input("Name")
        ticker = st.text_input("Ticker")
        exchange = st.text_input("Exchange")
        price = st.number_input("Price", min_value=0.01)
        submitted = st.form_submit_button("Add Product")

        if submitted and name and ticker and exchange:
            session.sql("""
                        INSERT INTO PRODUCTS (NAME, TICKER, EXCHANGE, PRICE)
                        VALUES (?, ?, ?)
                        """, 
                        params=[name, ticker, price]).collect()
            
            st.success("Product added!")
            st.rerun()

    with prod_right.form("del_product"):
        prod_id = st.text_input("Product ID")
        if st.form_submit_button("Delete Product") and prod_id:
            session.sql("DELETE FROM PRODUCTS WHERE PRODUCT_ID = ?", params=[prod_id]).collect()
            session.sql("DELETE FROM ORDERS WHERE PRODUCT_ID = ?", params=[prod_id]).collect()
            st.success(f"Deleted product with ID {prod_id}")
            st.rerun()


def main():
    st.title("Streamlit in Snowflake Test")

    # Set up columns for buttons
    button_cols = st.columns([1, 1, 1, 1])

    # Initialize session state
    if "stage" not in st.session_state:
        st.session_state.stage = 0

    # Button actions to update stage
    if button_cols[0].button("Show Customers"):
        st.session_state.stage = 1
    if button_cols[1].button("Show Orders"):
        st.session_state.stage = 2
    if button_cols[2].button("Show Products"):
        st.session_state.stage = 3

    # Display the appropriate section based on stage
    if st.session_state.stage == 1:
        show_customers()
    elif st.session_state.stage == 2:
        show_orders()
    elif st.session_state.stage == 3:
        show_products()


if __name__ == "__main__":
    main()