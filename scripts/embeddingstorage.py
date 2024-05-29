import json
import boto3
from botocore.exceptions import NoCredentialsError

# Initialize the S3 client
s3 = boto3.client('s3')

def upload_to_s3(bucket_name, key, data):
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))
        print(f"Successfully uploaded {key} to {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")

def store_embeddings_in_s3(embeddings, bucket_name, prefix="embeddings/"):
    for idx, embedding in enumerate(embeddings):
        key = f"{prefix}embedding_{idx}.json"
        upload_to_s3(bucket_name, key, embedding)

# Example usage
bucket_name = 'your-s3-bucket-name'
embeddings = [
    {'text': 'chunk1', 'embedding': [0.01977849006652832, 0.006099482532590628, ...]},
    {'text': 'chunk2', 'embedding': [0.021700561046600342, -0.008543084375560284, ...]},
    # add more embeddings as needed
]

store_embeddings_in_s3(embeddings, bucket_name)
