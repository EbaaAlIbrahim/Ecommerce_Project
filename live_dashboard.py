import sqlite3
import pandas as pd
import time
import os

print(" [Data Analyst] Initializing Live Business Intelligence Dashboard...")
print(" Opening active reporting interface. Press Ctrl+C to exit.\n")

DATABASE_FILE = r"C:\Users\Ebaa\Ecommerce_Project\ecommerce_warehouse.db"

try:
    while True:
        # 1. Clear the command prompt screen for an auto-refresh look
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("============================================================")
        print(f" REAL-TIME E-COMMERCE OPERATIONAL COMMAND DASHBOARD 🌟")
        print(f"  Last Refreshed: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("============================================================\n")
        
        # 2. Connect to the warehouse database
        connection = sqlite3.connect(DATABASE_FILE)
        
        # Query A: Calculate Live Cumulative Financial Performance
        financial_query = """
        SELECT 
            COUNT(CASE WHEN action = 'click' THEN 1 END) AS total_clicks,
            COUNT(CASE WHEN action = 'purchase' THEN 1 END) AS total_purchases,
            ROUND(SUM(CASE WHEN action = 'purchase' THEN 50.0 ELSE 0 END), 2) AS estimated_revenue
        FROM streaming_user_activity
        """
        # Note: We use a fixed $50.0 value per item to simulate rapid stream revenue calculations
        
        df_financials = pd.read_sql_query(financial_query, connection)
        
        # Query B: Live Regional Performance Analysis
        regional_query = """
        SELECT 
            region,
            COUNT(CASE WHEN action = 'purchase' THEN 1 END) AS units_sold,
            COUNT(CASE WHEN action = 'click' THEN 1 END) AS user_clicks
        FROM streaming_user_activity
        WHERE region != 'Unknown'
        GROUP BY region
        ORDER BY units_sold DESC
        """
        
        df_regions = pd.read_sql_query(regional_query, connection)
        connection.close()
        
        # 3. Print the live KPI cards to the business stakeholders
        if not df_financials.empty:
            clicks = df_financials['total_clicks'].values[0]
            purchases = df_financials['total_purchases'].values[0]
            revenue = df_financials['estimated_revenue'].values[0] or 0.00
            
            # Calculate conversion rate: what percentage of clicks became buys?
            conversion_rate = (purchases / clicks * 100) if clicks > 0 else 0.0
            
            print(" LIVE PLATFORM KEY PERFORMANCE INDICATORS (KPIs)")
            print("------------------------------------------------------------")
            print(f"  Total User Traffic  : {clicks:,} active clicks")
            print(f"  Total Orders Placed : {purchases:,} successful checkouts")
            print(f" Gross Est. Revenue   : ${revenue:,.2f}")
            print(f" Traffic Conversion   : {conversion_rate:.2f}%")
            print("------------------------------------------------------------\n")
            
        # 4. Print the live geographical matrix summary table
        print(" LIVE REGIONAL MARKET DISTRIBUTION")
        print("------------------------------------------------------------")
        if not df_regions.empty and df_regions['units_sold'].sum() > 0:
            print(df_regions.to_string(index=False))
        else:
            print(" Waiting for initial streaming transactions to register...")
        print("------------------------------------------------------------\n")
        
        print(" Tip: Watch this window alongside your Data Engineering script")
        print("   to see metrics increment instantly as live traffic streams in.")
        
        # 5. Delay execution for 2 seconds before running the analytics loop again
        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n Live Business Intelligence dashboard successfully shut down.")
