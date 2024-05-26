import requests
import json

# Get Symbl.ai authentication token
url = "https://api.symbl.ai/oauth2/token:generate"
payload = {
    "type": "application",
    "appId": "38716158656e6c4a4b725a7042695a5064477447386c733235644c346d487a62",
    "appSecret": "53474e38415266727a5f76526f6e797666674645497158506342586b4c47563541494d37716f2d6a79647a32546a43745f674767334c4576755377345a795630"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
auth_token = response.json()['accessToken']
print("Auth Token:", auth_token)

# Transcribe and analyze audio data
audio_url = "<your-audio-file-url>"
symbl_url = "https://api.symbl.ai/v1/process/audio/url"

payload = {
    "url": audio_url,
    "name": "Phone Call",
    "confidenceThreshold": 0.6,
    "detectEntities": True,
    "timezoneOffset": 0,
    "customVocabulary": ["word1", "word2"]
}
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

response = requests.post(symbl_url, json=payload, headers=headers)
print(response.json())

# Extract insights and sentiment analysis
conversation_id = "<conversation-id>"

insights_url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/insights"
headers = {
    "Authorization": f"Bearer {auth_token}"
}
response = requests.get(insights_url, headers=headers)
print(response.json())

sentiment_url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/messages"
response = requests.get(sentiment_url, headers=headers)
print(response.json())
