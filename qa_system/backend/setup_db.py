import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
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

# Step 3: Create Tables
tables = [
    """
    CREATE TABLE IF NOT EXISTS customer_data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(15),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customer_data(id),
        product_id INT REFERENCES products(id),
        quantity INT NOT NULL,
        total_price DECIMAL(10,2) NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
]

for table in tables:
    cur.execute(table)

print("Tables created successfully!")

# Step 4: Insert Sample Data
sample_data = [
    "INSERT INTO customer_data (name, email, phone) VALUES ('Alice Johnson', 'alice@example.com', '1234567890') ON CONFLICT DO NOTHING;",
    "INSERT INTO customer_data (name, email, phone) VALUES ('Bob Smith', 'bob@example.com', '0987654321') ON CONFLICT DO NOTHING;",
    "INSERT INTO customer_data (name, email, phone) VALUES ('Charlie Brown', 'charlie@example.com', '1112223333') ON CONFLICT DO NOTHING;",

    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('iPhone 15', 'Electronics', 999.99, 10) ON CONFLICT DO NOTHING;",
    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('MacBook Pro', 'Electronics', 1999.99, 5) ON CONFLICT DO NOTHING;",
    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Samsung TV', 'Electronics', 799.99, 8) ON CONFLICT DO NOTHING;",
    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Headphones', 'Accessories', 199.99, 20) ON CONFLICT DO NOTHING;",
    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Dell Laptop', 'Electronics', 899.99, 7) ON CONFLICT DO NOTHING;",
    "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Office Chair', 'Furniture', 149.99, 15) ON CONFLICT DO NOTHING;",

    "INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (1, 1, 1, 999.99) ON CONFLICT DO NOTHING;",
    "INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (1, 2, 1, 1999.99) ON CONFLICT DO NOTHING;",
    "INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (2, 3, 1, 799.99) ON CONFLICT DO NOTHING;",
    "INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (2, 4, 2, 399.98) ON CONFLICT DO NOTHING;",
    "INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (3, 5, 1, 899.99) ON CONFLICT DO NOTHING;"
]

for data in sample_data:
    cur.execute(data)

print("Sample data inserted successfully!")

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("Database setup completed!")
