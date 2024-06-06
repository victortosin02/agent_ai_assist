import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

nebula_api_key = os.getenv('NEBULA_API_KEY')

def get_embeddings(text):
    url = "https://api.symbl.ai/v1/embeddings"
    headers = {
        'x-api-key': nebula_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        embeddings = response.json()
        print("Embeddings:", embeddings)
        return embeddings
    else:
        print(f"Failed to get embeddings: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    text = "Your text here"
    get_embeddings(text)
