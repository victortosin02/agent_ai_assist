import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()

nebula_api_key = os.getenv('NEBULA_API_KEY')

def assist_agent(messages, system_prompt="You are a sales coaching assistant. You help user to get better at selling. You are respectful, professional and you always respond politely."):
    url = "https://api-nebula.symbl.ai/v1/model/chat/streaming"
    headers = {
        'ApiKey': nebula_api_key,
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        "max_new_tokens": 1024,
        "system_prompt": system_prompt,
        "messages": messages
    })

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print(f"Failed to get response: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    messages = [
        {
            "role": "human",
            "text": "Hello, I am Mark."
        },
        {
            "role": "assistant",
            "text": "Hello, Mark. I'm here to assist you with any sales-related questions or topics you'd like to discuss. How can I help you today?"
        },
        {
            "role": "human",
            "text": "Give me some tips on how do I improve in handling objections. Here is my transcript:\nMark: Hello, I am Mark from DataFlyte. How are you doing?\nCustomer: Hi, I am good. ....."
        }
    ]
    assist_agent(messages)
