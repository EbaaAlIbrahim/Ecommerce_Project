import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime, timedelta

fake = Faker()
random.seed(10)  # Seed gives us consistent random numbers

# Create raw data folder
os.makedirs("raw_data", exist_ok=True)

print("⏳ Step 1: Generating messy e-commerce logs...")

# 1. Create a base list of 50 products
products = []
categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty']
for i in range(1, 51):
    products.append({
        "product_id": f"PROD_{i:03d}",
        "product_name": fake.catch_phrase(),
        "category": random.choice(categories),
        "price": round(random.uniform(10.0, 500.0), 2)
    })
df_inventory = pd.DataFrame(products)

# 2. Create 1,000 messy website activity logs (Clicks & Purchases)
logs = []
start_date = datetime.now()

for _ in range(1000):
    user_id = f"USER_{random.randint(1, 200):03d}"
    product = random.choice(products)
    action = random.choices(['click', 'purchase'], weights=[0.8, 0.2])[0]
    timestamp = start_date + timedelta(minutes=random.randint(1, 43200))
    
    logs.append({
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "product_id": product["product_id"],
        # PROBLEM 1: Adding messy brackets/quotes to the text formatting
        "action": f"['{action}']", 
        # PROBLEM 2: Leaving some regions blank (None) on purpose
        "region": random.choices(['Riyadh', 'Dubai', 'Cairo', None], weights=[0.4, 0.4, 0.15, 0.05])[0]
    })

df_logs = pd.DataFrame(logs)

# PROBLEM 3: Injecting 40 exact duplicate rows to simulate server bugs
df_logs = pd.concat([df_logs, df_logs.sample(40)], ignore_index=True)

# Save messy data to files
df_inventory.to_csv("raw_data/raw_inventory.csv", index=False)
df_logs.to_csv("raw_data/raw_user_activity.csv", index=False)

print(" Success! Raw files saved in the 'raw_data' folder.")
print(f" Total Products: {len(df_inventory)}")
print(f" Total Activity Logs (including server duplicates): {len(df_logs)}")
