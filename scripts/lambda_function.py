import base64
import json

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        print("Decoded payload: " + str(payload))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
