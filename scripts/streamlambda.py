import boto3
import json

def lambda_handler(event, context):
    kinesis = boto3.client('kinesis')
    
    # Assuming 'Audio' is already base64 encoded in the event
    audio_data = event['Details']['ContactData']['MediaStreams']['Customer']['Audio']
    
    try:
        response = kinesis.put_record(
            StreamName='ConnectAudioStream',
            Data=audio_data,
            PartitionKey='partitionKey'
        )
        print("PutRecord Response: ", response)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Audio streaming started')
        }
        
    except Exception as e:
        print("Error putting record into Kinesis: ", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error streaming audio')
        }