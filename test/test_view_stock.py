import requests
import json

# Define the base URL of your API
base_url = "http://localhost:8000/api/view_current_stock"

response = requests.get(base_url + "/Notebook")