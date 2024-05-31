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

# Precomputed embeddings for troubleshooting phrases
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

# Function to assist agents based on triggers
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

# Function to send real-time assistance
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
    while True:
        records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)
        shard_iterator = records_response['NextShardIterator']

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