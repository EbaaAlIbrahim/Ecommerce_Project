import time
import random
import json
from datetime import datetime

# Setup static products and regions to simulate our market catalog
PRODUCTS = [f"PROD_{i:03d}" for i in range(1, 51)]
REGIONS = ['Riyadh', 'Dubai', 'Cairo', None] # None simulates a broken GPS sensor

print(" [Web Server] Starting continuous e-commerce stream simulation...")
print(" Broadcasting live user logs. Press Ctrl+C to terminate the server.\n")

# Use a standard text file as our streaming communication channel (Shock Absorber)
STREAM_FILE = "live_stream_buffer.json"

# Clear out any old streaming history to start completely fresh
with open(STREAM_FILE, "w") as f:
    pass

log_counter = 0

try:
    while True:
        log_counter += 1
        user_id = f"USER_{random.randint(1, 200):03d}"
        product_id = random.choice(PRODUCTS)
        action = random.choices(['click', 'purchase'], weights=[0.8, 0.2])[0]
        region = random.choices(REGIONS, weights=[0.4, 0.4, 0.15, 0.05])[0]
        
        # Build the payload mimicking raw web log data
        event_payload = {
            "event_id": f"EVT_{random.randint(100000, 999999)}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "product_id": product_id,
            "action": f"['{action}']",  # INTENTIONAL ISSUE: Messy bracket formatting
            "region": region
        }
        
        # Convert dictionary to raw text JSON string
        json_string = json.dumps(event_payload)
        
        # Append the line straight into our live stream buffer
        with open(STREAM_FILE, "a") as f:
            f.write(json_string + "\n")
            
        print(f" Broadcasted Event #{log_counter}: {action} on {product_id}")
        
        # Simulate network glitch: 5% chance the server repeats the exact same log entry
        if random.random() < 0.05:
            with open(STREAM_FILE, "a") as f:
                f.write(json_string + "\n")
            print(f"  [ glitch ] Server duplicated Event #{log_counter} to stream.")

        # Control the traffic speed: wait 1 second before emitting the next live customer event
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n Server simulator gracefully shut down.")
