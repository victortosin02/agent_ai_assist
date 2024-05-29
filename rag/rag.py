import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# AWS S3 Client Initialization
s3 = boto3.client('s3')

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

# Main function
def main():
    # Example text chunks to embed
    texts = [
        "Dan: Definitely, John. The first feature we're introducing ....",
        "Customer: Can you tell me more about the pricing?",
        # Add more text chunks as needed
    ]

    # Get embeddings for each text chunk
    embeddings = []
    for text in texts:
        embedding = get_embedding(text)
        if embedding:
            embeddings.append({'text': text, 'embedding': embedding})

    # Example of calculating similarity (optional)
    if len(embeddings) >= 2:
        similarity = calculate_similarity(embeddings[0]['embedding'], embeddings[1]['embedding'])
        print(f"Similarity between first two embeddings: {similarity}")

    # Store embeddings in S3
    bucket_name = 'your-s3-bucket-name'
    store_embeddings_in_s3(embeddings, bucket_name)

if __name__ == "__main__":
    main()
