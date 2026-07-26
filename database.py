import sqlite3

connection = sqlite3.connect("inventory.db")
cursor = connection.cursor()

# Materials
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    quantity REAL NOT NULL DEFAULT 0,
    price REAL NOT NULL,
    minimum_stock REAL NOT NULL DEFAULT 0
)
""")

# Products
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    selling_price REAL NOT NULL,
    description TEXT
)
""")

# Bill of Materials
cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_of_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    amount_needed REAL NOT NULL,

    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(material_id) REFERENCES materials(id)
)
""")

# Customer
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS customers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     phone TEXT,
#     email TEXT,
#     address TEXT
# )
# """)

# Orders
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_code TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    order_date TEXT NOT NULL,
    total REAL NOT NULL
)
""")

# Order Items
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    selling_price REAL NOT NULL,

    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

connection.commit()
connection.close()

print("Database initialized successfully!")