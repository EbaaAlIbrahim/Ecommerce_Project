import pandas as pd
import os

print(" Step 2: Starting the Data Cleaning Phase...")

# Create clean data folder if it doesn't exist
os.makedirs("clean_data", exist_ok=True)

# 1. Load the messy raw data files
df_inventory = pd.read_csv("raw_data/raw_inventory.csv")
df_logs = pd.read_csv("raw_data/raw_user_activity.csv")

# Note the number of rows before cleaning
initial_log_count = len(df_logs)

# 2. Fix formatting: Turn "['click']" or "['purchase']" into just "click" or "purchase"
df_logs['action'] = df_logs['action'].str.replace(r"[\[\]']", "", regex=True)

# 3. Remove duplicate entries caused by server bugs
df_logs = df_logs.drop_duplicates()
dropped_duplicates = initial_log_count - len(df_logs)

# 4. Fill missing regional values with 'Unknown' so there are no blank holes
df_logs['region'] = df_logs['region'].fillna("Unknown")

# 5. Save the perfectly clean files to a separate folder
df_inventory.to_csv("clean_data/clean_inventory.csv", index=False)
df_logs.to_csv("clean_data/clean_user_activity.csv", index=False)

print("\n Cleaning Complete!")
print(f" Detected and deleted {dropped_duplicates} duplicate server logs.")
print(f" Handled missing data by filling blank regions with 'Unknown'.")
print(f" Saved pristine files to the 'clean_data/' folder.")
