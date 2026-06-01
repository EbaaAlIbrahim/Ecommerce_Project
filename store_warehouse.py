import pandas as pd
import sqlite3

print(" Step 3: Initializing SQL Data Warehouse Pipeline...")

# 1. Load the clean CSV data into Python memory
df_inventory = pd.read_csv("clean_data/clean_inventory.csv")
df_logs = pd.read_csv("clean_data/clean_user_activity.csv")

# 2. Connect to SQLite (Creates 'ecommerce_warehouse.db' file instantly)
connection = sqlite3.connect("ecommerce_warehouse.db")
cursor = connection.cursor()

# 3. Create the Inventory table structure
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

# 4. Create the User Activity table structure
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_activity (
    timestamp TEXT,
    user_id TEXT,
    product_id TEXT,
    action TEXT,
    region TEXT,
    FOREIGN KEY (product_id) REFERENCES inventory (product_id)
)
""")

# 5. Load the clean dataframes directly into our SQL database tables
df_inventory.to_sql("inventory", connection, if_exists="replace", index=False)
df_logs.to_sql("user_activity", connection, if_exists="replace", index=False)

# Commit changes and close connection safely
connection.commit()
connection.close()

print(" Success! The Data Warehouse 'ecommerce_warehouse.db' is up and running.")
print(" Your clean data is now securely stored in relational SQL tables.")
