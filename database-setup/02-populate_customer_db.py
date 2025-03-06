import random
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
from faker import Faker

def main(session: snowpark.Session): 
    
    fake = Faker()
    
    session.sql("USE DATABASE CUSTOMER_DB;").collect()

    # Populate Customers table
    for _ in range(100):
        name = fake.name()
        email = fake.email()
        address = fake.address().replace("\n", ", ")
    
        session.sql(f"INSERT INTO CUSTOMERS (NAME, EMAIL, ADDRESS) VALUES ('{name}', '{email}', '{address}');").collect()

    # Populate Products table
    products = [
        ("Laptop", "Electronics", 999.99),
        ("Smartphone", "Electronics", 599.99),
        ("Headphones", "Accessories", 99.99),
        ("Tablet", "Electronics", 399.99),
        ("Backpack", "Fashion", 49.99)
    ]

    for name, category, price in products:
        session.sql(f"INSERT INTO PRODUCTS (NAME, CATEGORY, PRICE) VALUES ('{name}', '{category}', {price});").collect()

    # Retrieve generated customer and product IDs
    customer_ids = [row[0] for row in session.sql("SELECT ID FROM CUSTOMERS;").collect()]
    product_data = {row[0]: (row[1], row[2]) for row in session.sql("SELECT PRODUCT_ID, NAME, PRICE FROM PRODUCTS;").collect()}  # Store product_id -> (name, price)

    # Populate Orders table
    for _ in range(100):
        customer_id = random.choice(customer_ids)

        product_id = random.choice(list(product_data.keys()))
        product_name, product_price = product_data[product_id]
        quantity = random.randint(1, 5)
        total_price = quantity * product_price
    
        session.sql(f"""
            INSERT INTO ORDERS (CUSTOMER_ID, PRODUCT_ID, QUANTITY, TOTAL_PRICE)
            VALUES ({customer_id}, {product_id}, {quantity}, {total_price});
        """).collect()

    return ""