import psycopg2
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\Shraddha\OneDrive\Documents\Desktop\Git 2025\january\AskDB\qa_system\.env")

# Database connection details
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connect to database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Fetch data from tables
tables = ["customer_data", "products", "orders"]
for table in tables:
    print(f"\nFetching data from {table}:")
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Close connection
cur.close()
conn.close()