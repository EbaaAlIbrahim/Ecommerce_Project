import pandas as pd

# Load the AI rules and the product dictionary
try:
    df_rules = pd.read_csv("clean_data/ai_recommendation_rules.csv")
    df_products = pd.read_csv("clean_data/clean_inventory.csv")
except FileNotFoundError:
    print(" Error: Missing required files. Make sure Step 4 ran successfully.")
    exit()

# Turn products into a dictionary for quick name lookups
product_lookup = dict(zip(df_products['product_id'], df_products['product_name']))

print("\n E-Commerce Recommendation Engine Active!")
print("===========================================")
print("Type a Product ID to see what your AI recommends (Example: PROD_001, PROD_002)")
print("Type 'exit' to quit.\n")

while True:
    input_id = input("Enter Product ID: ").strip().upper()
    
    if input_id == 'EXIT':
        print("Goodbye!")
        break
        
    if input_id not in product_lookup:
        print(" Invalid ID. Please enter an ID between PROD_001 and PROD_050.")
        continue
    
    print(f"\n Selected Item: {product_lookup[input_id]} ({input_id})")
    
    # Filter rules for our selected product
    item_recommendations = df_rules[df_rules['product_id_x'] == input_id].head(3)
    
    if item_recommendations.empty:
        print(" The AI hasn't seen this item bought with anything else yet. Try another ID!")
    else:
        print(" Customers who bought this also bought:")
        for idx, row in item_recommendations.iterrows():
            rec_id = row['product_id_y']
            rec_name = product_lookup.get(rec_id, "Unknown Product")
            strength = row['recommendation_strength']
            print(f"     {rec_name} ({rec_id}) | Score: {strength}")
    print("-" * 50)
