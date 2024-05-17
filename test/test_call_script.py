import requests
import random
import json

# Define the base URL of your API
# base_url = "http://localhost:8000"
base_url = "http://34.244.139.0:8000"

# Define a set of possible items
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

# Function to randomly make a valid or invalid API call
def make_random_api_call():
    # Select a random item and determine if the call should be valid
    item = random.choice(items)
    is_valid_call = random.choices([True, False], weights=[95, 5])[0]

    # Modify the item for an invalid call
    if not is_valid_call:
        item['product_quantity'] = -1  # Set quantity to a negative number for invalidity

    # Define endpoints with weights
    endpoints = {
        "/api/add_new_item": 30,
        "/api/update_stock_item_number": 30,
        "/api/view_current_stock": 30,
        "/api/delete_item": 10  # Lower weight for delete
    }
    
    # Choose a random endpoint based on weights
    endpoint = random.choices(list(endpoints.keys()), weights=list(endpoints.values()), k=1)[0]
    url = f"{base_url}{endpoint}"

    # Adjust URL for GET and DELETE requests
    if endpoint == "/api/view_current_stock" or endpoint == "/api/delete_item":
        url += f"/{item['product_name']}"

    # Send request based on the method
    headers = {'Content-Type': 'application/json'}
    if endpoint in ["/api/add_new_item", "/api/update_stock_item_number"]:
        response = requests.post(url, json=item, headers=headers)
    elif endpoint == "/api/view_current_stock":
        response = requests.get(url, headers=headers)
    elif endpoint == "/api/delete_item":
        response = requests.delete(url, headers=headers)
        print(f"Deleted {item['product_name']} with status {response.status_code}")
        # Call the add endpoint after delete
        if response.status_code == 200:
            add_url = f"{base_url}/api/add_new_item"
            add_response = requests.post(add_url, json=item, headers=headers)
            print(f"Re-added {item['product_name']} with status {add_response.status_code}")

    # Print the results
    print(f"Endpoint: {endpoint}")
    print(f"Method: {'POST' if endpoint in ['/api/add_new_item', '/api/update_stock_item_number'] else 'GET' if endpoint == '/api/view_current_stock' else 'DELETE'}")
    print(f"Valid Call: {is_valid_call}")
    print(f"Payload: {item if endpoint in ['/api/add_new_item', '/api/update_stock_item_number'] else 'N/A'}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

# Make a random API call
make_random_api_call()
