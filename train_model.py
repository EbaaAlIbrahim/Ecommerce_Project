import pandas as pd
import sqlite3
import os

print(" [Data Scientist] Training recommendation rules matrix...")
DATABASE_FILE = r"C:\Users\Ebaa\Ecommerce_Project\ecommerce_warehouse.db"
OUTPUT_FILE = r"C:\Users\Ebaa\Ecommerce_Project\clean_data\ai_recommendation_rules.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

try:
    # 1. Connect to the warehouse database
    connection = sqlite3.connect(DATABASE_FILE)
    
    # 2. Extract purchase history records using SQL
    query = "SELECT user_id, product_id FROM streaming_user_activity WHERE action = 'purchase'"
    df_purchases = pd.read_sql_query(query, connection)
    connection.close()

    if df_purchases.empty:
        print(" No purchases found in the live database yet. Please ensure windows 1 & 2 are running to generate data first!")
        exit()

    print(f" Extracted {len(df_purchases)} real transactions. Calculating item pairs...")

    # 3. Perform a Self-Join to find items bought together by the same user
    df_pairs = df_purchases.merge(df_purchases, on='user_id')
    df_pairs = df_pairs[df_pairs['product_id_x'] != df_pairs['product_id_y']]

    # 4. Count the frequency of product pairings (Recommendation Strength)
    recommendations = df_pairs.groupby(['product_id_x', 'product_id_y']).size().reset_index(name='recommendation_strength')
    recommendations = recommendations.sort_values(by=['product_id_x', 'recommendation_strength'], ascending=[True, False])

    # 5. Export the trained rulebook out to disk
    recommendations.to_csv(OUTPUT_FILE, index=False)
    print(" Success! AI rules matrix generated successfully.")
    print(f" Saved to: {OUTPUT_FILE}")

except Exception as e:
    print(f" Error training model: {e}")
    print("Ensure window 2 (streaming_pipeline.py) has run at least once to create the data tables.")
