import requests

API_URL = "http://localhost:8000/chat"

# Example chat message
payload = {
    "message": "Hello, what can you tell me about the Gemma model?",
    # "system_prompt": "You are a helpful assistant."  # Optional
}

response = requests.post(API_URL, json=payload)

if response.ok:
    print("Model response:")
    print(response.json()["response"])
else:
    print(f"Error: {response.status_code}")
    print(response.text) 