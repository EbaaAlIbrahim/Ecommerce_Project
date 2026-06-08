import json
import sqlite3
import time
import os

print(" [Data Engineer] Initializing Always-On Streaming Pipeline...")

STREAM_FILE = "live_stream_buffer.json"
DATABASE_FILE = r"C:\Users\Ebaa\Ecommerce_Project\ecommerce_warehouse.db"

# A memory cache to track event IDs processed in the last few minutes (Deduplication)
processed_event_ids = set()

# Initialize Database tables if they were deleted
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS streaming_user_activity (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT,
    user_id TEXT,
    product_id TEXT,
    action TEXT,
    region TEXT
)
""")
connection.commit()
connection.close()

# Ensure the streaming buffer file exists so our script doesn't crash on launch
if not os.path.exists(STREAM_FILE):
    with open(STREAM_FILE, "w") as f:
        pass

print(" Pipeline Active. Watching the live stream for new data...\n")

# Open the file and hold the line position pointer
with open(STREAM_FILE, "r") as f:
    # Move the pointer to the very end of the file so we only process new data
    f.seek(0, os.SEEK_END)
    
    try:
        while True:
            # Try to read the next new line of text from the stream
            line = f.readline()
            
            # If no new data has arrived, rest for a fraction of a second and check again
            if not line:
                time.sleep(0.1)
                continue
                
            try:
                # PHASE 1 & 2: Ingest and Parse JSON string
                raw_event = json.loads(line.strip())
                event_id = raw_event["event_id"]
                
                # PHASE 3: Real-Time Transformation & Deduplication Check
                if event_id in processed_event_ids:
                    print(f"  [Deduplicated] Dropped duplicate Event: {event_id}")
                    continue
                    
                # Fix bracket formatting: "['click']" -> "click"
                clean_action = raw_event["action"].replace("[", "").replace("]", "").replace("'", "")
                
                # Handle Missing Data: None -> "Unknown"
                clean_region = raw_event["region"] if raw_event["region"] is not None else "Unknown"
                
                # Add current ID to our memory cache to prevent future duplicates
                processed_event_ids.add(event_id)
                # Keep cache small so it doesn't slow down computer memory
                if len(processed_event_ids) > 500:
                    processed_event_ids.pop()
                    
                # PHASE 4: Stream and Store straight into SQL Warehouse
                conn = sqlite3.connect(DATABASE_FILE)
                curr = conn.cursor()
                curr.execute("""
                INSERT OR IGNORE INTO streaming_user_activity (event_id, timestamp, user_id, product_id, action, region)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (event_id, raw_event["timestamp"], raw_event["user_id"], raw_event["product_id"], clean_action, clean_region))
                conn.commit()
                conn.close()
                
                print(f" [Stored] Event {event_id} | User: {raw_event['user_id']} | Action: {clean_action} | Region: {clean_region}")
                
            except Exception as json_err:
                print(f" Error parsing individual stream line: {json_err}")
                
    except KeyboardInterrupt:
        print("\n Streaming pipeline safely shut down.")
