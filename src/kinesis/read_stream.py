import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

kinesis_stream_name = os.getenv('KINESIS_STREAM_NAME')

def read_stream():
    kinesis = boto3.client('kinesis')
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=kinesis_stream_name,
        ShardId='shardId-000000000000',
        ShardIteratorType='LATEST'
    )['ShardIterator']

    while True:
        records = kinesis.get_records(ShardIterator=shard_iterator, Limit=100)
        for record in records['Records']:
            print(record['Data'])
        shard_iterator = records['NextShardIterator']

if __name__ == "__main__":
    read_stream()
