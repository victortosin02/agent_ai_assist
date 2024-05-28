import requests
import json

NEBULA_API_KEY="YOUR_API_KEY"

url = "https://api-nebula.symbl.ai/v1/model/chat/streaming"

payload = json.dumps({
  "max_new_tokens": 1024,
  "system_prompt": "You are a service support assistant. You help user to troubleshoot issues with purchased products and services. You are respectful, professional and you always respond politely.",
  "messages": [
    {
      "role": "human",
      "text": "Hello, I am Mark."
    },
    {
      "role": "assistant",
      "text": "Hello, Mark. I'm here to assist you with any product related questions or topics you'd like to discuss. How can I help you today?"
    },
    {
      "role": "human",
      "text": "The service I subscribe to is not working. Can you tell me what is going on because I can't seem to use the service"
    }
  ]
})
headers = {
  'ApiKey': NEBULA_API_KEY,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
