import requests
import json

# Define the base URL of your API
base_url = "http://localhost:8000/api/add_new_item"
# Define a list of possible items
items = [
    {"item_id": "001", "product_name": "Widget", "manufacturer": "Widgets Inc.", "product_quantity": 50},
    {"item_id": "002", "product_name": "Gadget", "manufacturer": "Gadgets Corp.", "product_quantity": 50},
    {"item_id": "003", "product_name": "Tool", "manufacturer": "Tools LLC", "product_quantity": 50},
    {"item_id": "004", "product_name": "Screwdriver", "manufacturer": "Hardware Co.", "product_quantity": 50},
    {"item_id": "005", "product_name": "Hammer", "manufacturer": "Hammer Time Ltd.", "product_quantity": 50},
    {"item_id": "006", "product_name": "Laptop", "manufacturer": "Tech Innovations", "product_quantity": 50},
    {"item_id": "007", "product_name": "Smartphone", "manufacturer": "Communications Inc.", "product_quantity": 50},
    {"item_id": "008", "product_name": "Tablet", "manufacturer": "Gadgetry Unlimited", "product_quantity": 50},
    {"item_id": "009", "product_name": "Headphones", "manufacturer": "Sound Enterprises", "product_quantity": 50},
    {"item_id": "010", "product_name": "Bluetooth Speaker", "manufacturer": "AudioWorks", "product_quantity": 50},
    {"item_id": "011", "product_name": "LED Monitor", "manufacturer": "Visual Tech", "product_quantity": 50},
    {"item_id": "012", "product_name": "Mouse", "manufacturer": "Computing Accessories Ltd.", "product_quantity": 50},
    {"item_id": "013", "product_name": "Keyboard", "manufacturer": "Typing Solutions", "product_quantity": 50},
    {"item_id": "014", "product_name": "Webcam", "manufacturer": "Tech Gear", "product_quantity": 50},
    {"item_id": "015", "product_name": "Desk Lamp", "manufacturer": "Bright Light Inc.", "product_quantity": 50},
    {"item_id": "016", "product_name": "Notebook", "manufacturer": "Office Supplies Co.", "product_quantity": 50},
    {"item_id": "017", "product_name": "Backpack", "manufacturer": "Travel Gear", "product_quantity": 50},
    {"item_id": "018", "product_name": "Water Bottle", "manufacturer": "Hydration Supplies", "product_quantity": 50},
    {"item_id": "019", "product_name": "Charger", "manufacturer": "Power Solutions", "product_quantity": 50},
    {"item_id": "020", "product_name": "Sunglasses", "manufacturer": "Fashion Specs", "product_quantity": 50}
]

def add_all_products():
    headers = {'Content-Type': 'application/json'}
    for item in items:
        response = requests.post(base_url, json=item, headers=headers)
        if response.status_code == 200:
            print(f"Successfully added item: {item['product_name']}")
        else:
            print(f"Failed to add item: {item['product_name']}. Response: {response.text}")

# Execute the function to add all products
add_all_products()
