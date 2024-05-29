import os
import requests
import json
import symbl
import boto3
from botocore.exceptions import NoCredentialsError
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

# AWS S3 Client Initialization
s3 = boto3.client('s3')

# Symbl.ai Credentials
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
PHONE_NUMBER = 'your_phone_number'
EMAIL = 'your_email'
ACCESS_TOKEN = 'your_access_token'

# Nebula API Key
NEBULA_API_KEY = 'your_nebula_api_key'

# Function to get embeddings from Nebula API
def get_embedding(text):
    url = "https://api-nebula.symbl.ai/v1/model/embed"
    headers = {
        "ApiKey": NEBULA_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        print(f"Failed to get embedding for text: {text}")
        return None

# Function to calculate cosine similarity between two embeddings
def calculate_similarity(embedding_1, embedding_2):
    embedding_1 = np.array(embedding_1)
    embedding_2 = np.array(embedding_2)
    similarity = cosine_similarity([embedding_1, embedding_2])
    return similarity[0][1]

# Function to upload data to S3
def upload_to_s3(bucket_name, key, data):
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))
        print(f"Successfully uploaded {key} to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")

# Function to store embeddings in S3
def store_embeddings_in_s3(embeddings, bucket_name, prefix="embeddings/"):
    for idx, embedding in enumerate(embeddings):
        key = f"{prefix}embedding_{idx}.json"
        upload_to_s3(bucket_name, key, embedding)

# Function to start telephony session and retrieve conversation ID
def start_telephony_session():
    connection_object = symbl.Telephony.start_pstn(
        credentials={"app_id": APP_ID, "app_secret": APP_SECRET},
        phone_number=PHONE_NUMBER,
        actions=[
            {
                "invokeOn": "stop",
                "name": "sendSummaryEmail",
                "parameters": {
                    "emails": [EMAIL],
                },
            },
        ]
    )
    return connection_object.conversation.get_conversation_id()

# Function to get real-time messages from the conversation
def get_real_time_messages(conversation_id):
    url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get("messages", [])

# Main function
def main():
    # Step 1: Start telephony session and get conversation ID
    print("Starting telephony session...")
    conversation_id = start_telephony_session()
    print(f"Conversation ID: {conversation_id}")

    # Step 2: Retrieve real-time messages from the conversation
    print("Retrieving real-time messages...")
    time.sleep(30)  # Wait for a while before polling
    messages = get_real_time_messages(conversation_id)
    
    if not messages:
        print("No messages retrieved from the conversation.")
        return

    # Step 3: Generate embeddings for the retrieved messages
    embeddings = []
    for message in messages:
        text = message.get("text")
        embedding = get_embedding(text)
        if embedding:
            embeddings.append({'text': text, 'embedding': embedding})

    # Step 4: Example of calculating similarity (optional)
    if len(embeddings) >= 2:
        similarity = calculate_similarity(embeddings[0]['embedding'], embeddings[1]['embedding'])
        print(f"Similarity between first two embeddings: {similarity}")

    # Step 5: Store embeddings in S3
    bucket_name = 'your-s3-bucket-name'
    store_embeddings_in_s3(embeddings, bucket_name)

if __name__ == "__main__":
    main()
