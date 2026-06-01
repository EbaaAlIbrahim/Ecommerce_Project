import pandas as pd
import sqlite3

print(" Step 4: Starting Data Science Engine...")

# 1. Connect to our SQL Data Warehouse
connection = sqlite3.connect("ecommerce_warehouse.db")

# 2. Extract only successful purchase records using SQL
query = """
SELECT user_id, product_id 
FROM user_activity 
WHERE action = 'purchase'
"""
df_purchases = pd.read_sql_query(query, connection)
connection.close()

print(f" Extracted {len(df_purchases)} purchase records for AI training.")

# 3. SELF-JOIN: Find products bought by the exact same users
# We merge the table with itself on the 'user_id' column
df_pairs = df_purchases.merge(df_purchases, on='user_id')

# 4. Filter out pairs where an item matches itself (e.g., PROD_001 with PROD_001)
df_pairs = df_pairs[df_pairs['product_id_x'] != df_pairs['product_id_y']]

# 5. Count how many times each unique product pair was bought together
recommendations = df_pairs.groupby(['product_id_x', 'product_id_y']).size().reset_index(name='recommendation_strength')

# 6. Sort them so the highest scores (strongest relationships) come first
recommendations = recommendations.sort_values(by=['product_id_x', 'recommendation_strength'], ascending=[True, False])

# Save our AI's rule book
recommendations.to_csv("clean_data/ai_recommendation_rules.csv", index=False)

print(" AI Recommendation Model trained successfully!")
print(" Rules saved to 'clean_data/ai_recommendation_rules.csv'.")
