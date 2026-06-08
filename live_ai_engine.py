import sqlite3
import pandas as pd
import time
import os

print(" [Data Scientist] Initializing Live Personalization Engine...")

DATABASE_FILE = r"C:\Users\Ebaa\Ecommerce_Project\ecommerce_warehouse.db"
RULES_FILE = "clean_data/ai_recommendation_rules.csv"

# 1. Load our trained AI recommendation rules template
if not os.path.exists(RULES_FILE):
    print(" Error: AI rules matrix not found. Please run Step 4 first to train the model!")
    exit()

df_rules = pd.read_csv(RULES_FILE)

# 2. Setup the Live Production Profile Store Table
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS live_user_recommendations (
    user_id TEXT PRIMARY KEY,
    last_purchased_item TEXT,
    recommended_product_1 TEXT,
    recommended_product_2 TEXT,
    timestamp TEXT
)
""")
connection.commit()
connection.close()

print(" AI Model loaded. Monitoring live warehouse for customer purchases...\n")

# Keep track of the last record we analyzed so we don't repeat computations
last_processed_timestamp = ""

try:
    while True:
        # 3. Query the warehouse for the single most recent purchase
        connection = sqlite3.connect(DATABASE_FILE)
        query = """
        SELECT timestamp, user_id, product_id 
        FROM streaming_user_activity 
        WHERE action = 'purchase'
        ORDER BY timestamp DESC 
        LIMIT 1
        """
        df_last_purchase = pd.read_sql_query(query, connection)
        connection.close()
        
        # If a purchase exists and it's brand new, process it
        if not df_last_purchase.empty:
            current_timestamp = df_last_purchase['timestamp'].values[0]
            user_id = df_last_purchase['user_id'].values[0]
            product_id = df_last_purchase['product_id'].values[0]
            
            if current_timestamp != last_processed_timestamp:
                print(f" [AI Triggered] Detected new purchase by {user_id}: {product_id}")
                
                # 4. Find the top 2 matching recommendations from our AI rules matrix
                matching_rules = df_rules[df_rules['product_id_x'] == product_id].head(2)
                
                rec1 = "None"
                rec2 = "None"
                
                # Assign recommendations if our model has seen this product paired before
                if len(matching_rules) > 0:
                    rec1 = matching_rules.iloc[0]['product_id_y']
                if len(matching_rules) > 1:
                    rec2 = matching_rules.iloc[1]['product_id_y']
                    
                # 5. Update the live profile store database instantly
                connection = sqlite3.connect(DATABASE_FILE)
                cursor = connection.cursor()
                cursor.execute("""
                INSERT OR REPLACE INTO live_user_recommendations 
                (user_id, last_purchased_item, recommended_product_1, recommended_product_2, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, product_id, rec1, rec2, current_timestamp))
                connection.commit()
                connection.close()
                
                print(f" [Live Profile Updated] {user_id} Homepage set to recommend: {rec1}, {rec2}")
                print("-" * 60)
                
                # Update our tracking marker
                last_processed_timestamp = current_timestamp
                
        # Wait half a second before checking the warehouse again
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n Live AI engine safely shut down.")
