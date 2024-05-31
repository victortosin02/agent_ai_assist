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
kinesis_client = boto3.client('kinesis')

# Symbl.ai Credentials
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
PHONE_NUMBER = 'your_phone_number'
EMAIL = 'your_email'
ACCESS_TOKEN = 'your_access_token'

# Nebula API Key
NEBULA_API_KEY = 'your_nebula_api_key'

# Troubleshooting phrases and their precomputed embeddings
troubleshooting_phrases = ["restart", "reboot", "reset", "troubleshoot", "error", "not working"]
troubleshooting_embeddings = [get_embedding(phrase) for phrase in troubleshooting_phrases]

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

# Function to provide real-time assistance
def assist_agent(transcription):
    text = transcription['text']
    current_embedding = get_embedding(text)

    for trigger_embedding in troubleshooting_embeddings:
        similarity = calculate_similarity(current_embedding, trigger_embedding)
        if similarity > 0.8:  # Threshold for considering it a match
            # Trigger real-time assistance (e.g., by sending a message to the agent)
            print(f"Troubleshooting phrase detected: {text}")
            send_real_time_assistance(text)
            break

def send_real_time_assistance(text):
    url = "https://api-nebula.symbl.ai/v1/model/chat/streaming"
    payload = json.dumps({
        "max_new_tokens": 1024,
        "system_prompt": "You are a service support assistant. You help users troubleshoot issues with purchased products and services. You are respectful, professional and you always respond politely.",
        "messages": [
            {
                "role": "human",
                "text": text
            }
        ]
    })
    headers = {
        'ApiKey': NEBULA_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())  # Real-time AI assistance response

# Continuously read from Kinesis stream and provide real-time assistance
def read_from_kinesis():
    response = kinesis_client.get_shard_iterator(
        StreamName='YourKinesisStreamName',
        ShardId='shardId-000000000000',
        ShardIteratorType='LATEST'
    )

    shard_iterator = response['ShardIterator']
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)

    for record in records_response['Records']:
        audio_chunk = record['Data']  # Extract the audio chunk

        # Send audio data to Symbl.ai for transcription
        symbl_response = requests.post(
            "https://api.symbl.ai/v1/process/audio",
            headers={
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'audio_url': 's3://your-audio-file-path'
            })
        )

        transcription = symbl_response.json()
        print(transcription)  # Print or process the transcription

        # Send transcription to Nebula LLM for real-time assistance
        assist_agent(transcription)

# Main function to continuously read from Kinesis stream
if __name__ == "__main__":
    while True:
        read_from_kinesis()
