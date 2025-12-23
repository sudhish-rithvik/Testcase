import requests
import json

API_KEY = "AIzaSyAdjcbkZXf9JpMOvlza7ro-IcSORGRNjnM"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))
