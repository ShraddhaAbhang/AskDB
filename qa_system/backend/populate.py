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
    ("Ava Thomas", "ava@example.com", "1010101010"),
    ("Sophia Martinez", "sophia.m@example.com", "9876543210"),
    ("Liam Anderson", "liam.a@example.com", "9876543211"),
    ("Olivia Thomas", "olivia.t@example.com", "9876543212"),
    ("Noah Johnson", "noah.j@example.com", "9876543213"),
    ("Emma Williams", "emma.w@example.com", "9876543214"),
    ("Mason Brown", "mason.b@example.com", "9876543215"),
    ("Isabella Lewis", "isabella.l@example.com", "9876543216"),
    ("Lucas Walker", "lucas.w@example.com", "9876543217"),
    ("Mia Hall", "mia.h@example.com", "9876543218"),
    ("Ethan Young", "ethan.y@example.com", "9876543219"),
    ("Ava Allen", "ava.a@example.com", "9876543220"),
    ("James King", "james.k@example.com", "9876543221"),
    ("Harper Scott", "harper.s@example.com", "9876543222"),
    ("Benjamin Adams", "benjamin.a@example.com", "9876543223"),
    ("Evelyn Nelson", "evelyn.n@example.com", "9876543224"),
    ("Henry Carter", "henry.c@example.com", "9876543225"),
    ("Charlotte Mitchell", "charlotte.m@example.com", "9876543226"),
    ("Alexander Perez", "alexander.p@example.com", "9876543227"),
    ("Amelia Roberts", "amelia.r@example.com", "9876543228"),
    ("William Green", "william.g@example.com", "9876543229"),
    ("Elijah Baker", "elijah.b@example.com", "9876543230"),
    ("Lucas Hill", "lucas.h@example.com", "9876543231"),
    ("Scarlett Adams", "scarlett.a@example.com", "9876543232"),
    ("Jackson Wright", "jackson.w@example.com", "9876543233"),
    ("Ella Turner", "ella.t@example.com", "9876543234"),
    ("David Collins", "david.c@example.com", "9876543235"),
    ("Sofia Stewart", "sofia.s@example.com", "9876543236"),
    ("Matthew Rogers", "matthew.r@example.com", "9876543237"),
    ("Lily Murphy", "lily.m@example.com", "9876543238"),
    ("Samuel Bell", "samuel.b@example.com", "9876543239"),
    ("Aria Lee", "aria.l@example.com", "9876543240"),
    ("Daniel Scott", "daniel.s@example.com", "9876543241"),
    ("Grace Rivera", "grace.r@example.com", "9876543242"),
    ("Michael Wood", "michael.w@example.com", "9876543243"),
    ("Victoria White", "victoria.w@example.com", "9876543244"),
    ("Joseph Harris", "joseph.h@example.com", "9876543245"),
    ("Chloe Martin", "chloe.m@example.com", "9876543246"),
    ("Gabriel Thompson", "gabriel.t@example.com", "9876543247"),
    ("Hannah Moore", "hannah.m@example.com", "9876543248"),
    ("Jackson Nelson", "jackson.n@example.com", "9876543249"),
    ("Avery Carter", "avery.c@example.com", "9876543250"),
    ("David Miller", "david.miller@example.com", "9001112233"),
    ("Sophia Lee", "sophia.lee@example.com", "9012223344"),
    ("James Anderson", "james.anderson@example.com", "9023334455"),
    ("Olivia Brown", "olivia.brown@example.com", "9034445566"),
    ("Liam Johnson", "liam.johnson@example.com", "9045556677"),
    ("Emma Wilson", "emma.wilson@example.com", "9056667788"),
    ("Noah Carter", "noah.carter@example.com", "9067778899"),
    ("Ava Martinez", "ava.martinez@example.com", "9078889900"),
    ("William Thomas", "william.thomas@example.com", "9089990011"),
    ("Mia White", "mia.white@example.com", "9090001122")
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
    ("Amazon Echo", "Smart Home", 99.99, 20),
    ("HP Laptop", "Electronics", 799.99, 12),
    ("Office Desk", "Furniture", 199.99, 20),
    ("iPad Air", "Electronics", 599.99, 15),
    ("Gaming Monitor", "Electronics", 299.99, 10),
    ("Yoga Mat", "Fitness", 49.99, 30),
    ("Running Shoes", "Clothing", 119.99, 25),
    ("Smart Bulb", "Home Appliances", 19.99, 50),
    ("Wireless Charger", "Accessories", 39.99, 35),
    ("Air Purifier", "Home Appliances", 149.99, 18),
    ("Leather Wallet", "Accessories", 79.99, 40),
    ("Electric Kettle", "Home Appliances", 29.99, 22),
    ("Bluetooth Keyboard", "Accessories", 59.99, 17),
    ("Noise Cancelling Headphones", "Electronics", 129.99, 11),
    ("Tablet Stand", "Accessories", 24.99, 35),
    ("Foldable Treadmill", "Fitness", 499.99, 5),
    ("Outdoor Grill", "Home Appliances", 349.99, 8),
    ("VR Headset", "Electronics", 699.99, 6),
    ("4K Smart TV", "Electronics", 899.99, 9),
    ("Portable Speaker", "Electronics", 89.99, 23),
    ("USB-C Hub", "Accessories", 29.99, 45),
    ("Google Pixel 8", "Electronics", 799.99, 10),
    ("AirPods Pro", "Accessories", 249.99, 20),
    ("Sony PS5", "Gaming", 499.99, 5),
    ("HP Spectre x360", "Electronics", 1299.99, 7),
    ("Ergonomic Desk", "Furniture", 199.99, 15),
    ("Samsung Galaxy S24", "Electronics", 1099.99, 12),
    ("Bose Noise Cancelling Headphones", "Accessories", 349.99, 18),
    ("Xbox Series X", "Gaming", 499.99, 6),
    ("Asus ROG Laptop", "Electronics", 1599.99, 5),
    ("Standing Desk", "Furniture", 299.99, 10)
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
