import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\Shraddha\OneDrive\Documents\Desktop\Git 2025\january\AskDB\qa_system\.env")

# Database connection details
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


# Connect to PostgreSQL (default database)
conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Allow CREATE DATABASE

# Create a cursor
cur = conn.cursor()

# Step 1: Create Database
try:
    cur.execute(f"CREATE DATABASE {DB_NAME};")
    print(f"Database '{DB_NAME}' created successfully!")
except psycopg2.errors.DuplicateDatabase:
    print(f"Database '{DB_NAME}' already exists.")
    
cur.close()
conn.close()

# Step 2: Connect to the new database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Step 4: Insert More Sample Data
# Insert Customers (20 customers)
customers = [
    ("John Doe", "john@example.com", "1111111111"),
    ("Emma Watson", "emma@example.com", "2222222222"),
    ("William Brown", "william@example.com", "3333333333"),
    ("Sophia Martinez", "sophia@example.com", "4444444444"),
    ("Michael Clark", "michael@example.com", "5555555555"),
    ("Sarah Johnson", "sarah@example.com", "6666666666"),
    ("David Lee", "david@example.com", "7777777777"),
    ("Olivia Adams", "olivia@example.com", "8888888888"),
    ("Ethan White", "ethan@example.com", "9999999999"),
    ("Ava Thomas", "ava@example.com", "1010101010")
]

for customer in customers:
    cur.execute("INSERT INTO customer_data (name, email, phone) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", customer)

# Insert Products (15 products)
products = [
    ("Google Pixel 7", "Electronics", 599.99, 15),
    ("HP Pavilion Laptop", "Electronics", 799.99, 12),
    ("Sony Headphones", "Accessories", 149.99, 30),
    ("Apple Watch", "Wearable", 399.99, 20),
    ("Gaming Chair", "Furniture", 249.99, 10),
    ("Samsung Galaxy S23", "Electronics", 999.99, 10),
    ("ASUS ROG Laptop", "Electronics", 1499.99, 7),
    ("Bose Speakers", "Audio", 199.99, 20),
    ("Office Desk", "Furniture", 299.99, 15),
    ("Canon DSLR", "Camera", 899.99, 5),
    ("Smart TV", "Electronics", 699.99, 8),
    ("Air Purifier", "Home Appliances", 129.99, 15),
    ("Wireless Keyboard", "Accessories", 49.99, 25),
    ("Gaming Mouse", "Accessories", 39.99, 30),
    ("Amazon Echo", "Smart Home", 99.99, 20)
]

for product in products:
    cur.execute("INSERT INTO products (name, category, price, stock_quantity) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;", product)

# Insert Orders (30 random orders)
for _ in range(30):
    customer_id = random.randint(1, len(customers))  # Random customer
    product_id = random.randint(1, len(products))  # Random product
    quantity = random.randint(1, 5)  # Random quantity (1-5)
    
    # Fetch product price
    cur.execute("SELECT price FROM products WHERE id = %s;", (product_id,))
    price = cur.fetchone()[0]
    
    total_price = price * quantity
    order_date = datetime.now() - timedelta(days=random.randint(1, 100))  # Random past date
    
    cur.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, total_price, order_date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
        (customer_id, product_id, quantity, total_price, order_date)
    )

print("More sample data inserted successfully!")

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("Database setup completed with more data!")