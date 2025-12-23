import requests
import json

API_KEY = "AIzaSyAdjcbkZXf9JpMOvlza7ro-IcSORGRNjnM"

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent"
    f"?key={API_KEY}"
)

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Say hello in one short sentence"}
            ]
        }
    ]
}

response = requests.post(url, json=payload, timeout=30)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))
