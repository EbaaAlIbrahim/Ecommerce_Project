import pandas as pd
import sqlite3

print(" Step 6: Initializing Data Analytics & Business Reports...")

# 1. Connect to our SQL Data Warehouse
connection = sqlite3.connect("ecommerce_warehouse.db")

# 2. Query 1: Top Performing Regions (Where is the revenue coming from?)
# This calculates total spending by grouping prices and regions together
region_query = """
SELECT 
    ua.region,
    COUNT(ua.product_id) AS total_items_sold,
    ROUND(SUM(i.price), 2) AS total_revenue
FROM user_activity ua
JOIN inventory i ON ua.product_id = i.product_id
WHERE ua.action = 'purchase' AND ua.region != 'Unknown'
GROUP BY ua.region
ORDER BY total_revenue DESC
"""

df_regions = pd.read_sql_query(region_query, connection)

# 3. Query 2: Product Popularity Report (Which categories dominate?)
category_query = """
SELECT 
    i.category,
    COUNT(ua.product_id) AS total_units_sold,
    ROUND(SUM(i.price), 2) AS total_revenue
FROM user_activity ua
JOIN inventory i ON ua.product_id = i.product_id
WHERE ua.action = 'purchase'
GROUP BY i.category
ORDER BY total_units_sold DESC
"""

df_categories = pd.read_sql_query(category_query, connection)
connection.close()

# 4. Display the visual reports directly to the business stakeholders
print("\n REPORT 1: REGIONAL SALES PERFORMANCE")
print("=======================================")
print(df_regions.to_string(index=False))

print("\n REPORT 2: PRODUCT CATEGORY POPULARITY")
print("=======================================")
print(df_categories.to_string(index=False))

# 5. Save the reports for the management team
df_regions.to_csv("clean_data/regional_sales_report.csv", index=False)
df_categories.to_csv("clean_data/category_sales_report.csv", index=False)
print("\n Reports successfully exported to CSV for the supply chain team!")
