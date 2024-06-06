import requests
import boto3
from botocore.exceptions import NoCredentialsError
import json
from utils.constants import NEBULA_API_KEY, S3_BUCKET_NAME

# Initialize the S3 client
s3 = boto3.client('s3')

def get_embedding(text):
    """
    Function to get embeddings from Nebula API.
    """
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

def upload_to_s3(bucket_name, key, data):
    """
    Function to upload data to S3.
    """
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))
        print(f"Successfully uploaded {key} to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")

def store_embeddings_in_s3(embeddings, bucket_name, prefix="embeddings/"):
    """
    Function to store embeddings in S3.
    """
    for idx, embedding in enumerate(embeddings):
        key = f"{prefix}embedding_{idx}.json"
        upload_to_s3(bucket_name, key, embedding)

if __name__ == "__main__":
    # Define the troubleshooting phrases
    troubleshooting_phrases = ["restart", "reboot", "reset", "troubleshoot", "error", "not working"]
    
    # Get embeddings for each phrase
    embeddings = [get_embedding(phrase) for phrase in troubleshooting_phrases]
    
    # Store the embeddings in the specified S3 bucket
    store_embeddings_in_s3(embeddings, S3_BUCKET_NAME)
