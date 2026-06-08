import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

print(" [Data Analyst] Initializing Full-Traffic Graphical Dashboard...")
DATABASE_FILE = r"C:\Users\Ebaa\Ecommerce_Project\ecommerce_warehouse.db"

# 1. Initialize the graphical plotting layout window
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
fig.canvas.manager.set_window_title('Live E-Commerce Analytics Control Room')

def refresh_visuals(frame):
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        
        # CHANGED QUERY: Track total traffic volume (clicks + buys) so bars populate instantly!
        regional_query = """
        SELECT region, COUNT(*) as total_activity
        FROM streaming_user_activity
        WHERE region != 'Unknown'
        GROUP BY region
        ORDER BY total_activity DESC
        """
        df_regions = pd.read_sql_query(regional_query, connection)
        
        # Query B: Fetch live user interaction counts
        action_query = """
        SELECT action, COUNT(*) as total_count
        FROM streaming_user_activity
        GROUP BY action
        """
        df_actions = pd.read_sql_query(action_query, connection)
        connection.close()

        # Wipe old drawings to prepare for the redraw
        ax1.clear()
        ax2.clear()

        # 4. Draw Graph 1: Bar Chart (Total Activity per City)
        if not df_regions.empty:
            bar_colors = ['#3498db', '#2ecc71', '#e74c3c'] # Blue, Green, Red
            ax1.bar(df_regions['region'], df_regions['total_activity'], color=bar_colors[:len(df_regions)])
            ax1.set_title("Live User Activity Volume by City", fontsize=11, fontweight='bold', pad=10)
            ax1.set_ylabel("Total Actions (Clicks + Purchases)")
            ax1.set_xlabel("Market Region")
        else:
            ax1.text(0.5, 0.5, "Waiting for stream data...", ha='center', va='center', color='gray')

        # 5. Draw Graph 2: Pie Chart (Clicks vs Buys)
        if not df_actions.empty:
            ax2.pie(
                df_actions['total_count'], 
                labels=df_actions['action'], 
                autopct='%1.1f%%', 
                startangle=140,
                colors=['#f1c40f', '#27ae60'] # Yellow for clicks, Green for purchases
            )
            ax2.set_title("Live Traffic Breakdown (Clicks vs Buys)", fontsize=11, fontweight='bold', pad=10)
        else:
            ax2.text(0.5, 0.5, "Waiting for traffic stream...", ha='center', va='center', color='gray')

        plt.tight_layout()

    except Exception as db_err:
        print(f" Database temporary lag: {db_err}")

# Kick off the Animation Loop (Refreshes every 2000 milliseconds)
global ani
ani = FuncAnimation(fig, refresh_visuals, interval=2000, cache_frame_data=False)

plt.tight_layout()
plt.show()
