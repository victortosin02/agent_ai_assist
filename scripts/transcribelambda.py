import requests
import json
import boto3

# Initialize the Kinesis client
kinesis_client = boto3.client('kinesis')

# Symbl.ai API credentials
symbl_api_key = 'your_symbl_api_key'

# Nebula API key
NEBULA_API_KEY = 'your_nebula_api_key'

# Define the troubleshooting tracker vocabulary
troubleshooting_vocabulary = ["restart", "reboot", "reset", "troubleshoot", "error", "not working"]

# Function to read data from Kinesis stream
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
                'Authorization': 'Bearer ' + symbl_api_key,
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'audio_url': 's3://your-audio-file-path'
            })
        )

        transcription = symbl_response.json()
        print(transcription)  # Print or process the transcription

        # Check if the transcription contains any troubleshooting keywords
        if any(word in transcription['text'].lower() for word in troubleshooting_vocabulary):
            # Send transcription to Nebula LLM for real-time assistance
            assist_agent(transcription['text'])

def assist_agent(transcription_text):
    url = "https://api-nebula.symbl.ai/v1/model/chat/streaming"
    payload = json.dumps({
        "max_new_tokens": 1024,
        "system_prompt": "You are a service support assistant. You help users troubleshoot issues with purchased products and services. You are respectful, professional and you always respond politely.",
        "messages": [
            {
                "role": "human",
                "text": transcription_text
            }
        ]
    })
    headers = {
        'ApiKey': NEBULA_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())  # Real-time AI assistance response

# Continuously read from Kinesis stream
while True:
    read_from_kinesis()
