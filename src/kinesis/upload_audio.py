import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

s3_bucket_name = os.getenv('de-victor-oladejo-source-file-gateway')

def upload_audio(file_path, file_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, s3_bucket_name, file_name)
        print(f"File {file_name} uploaded successfully to {s3_bucket_name}.")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    file_path = 'path_to_your_audio_file'
    file_name = 'your_audio_file_name'
    upload_audio(file_path, file_name)
