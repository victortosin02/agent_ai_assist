## Real-Time AI Assistance for Call Center Agents

## Introduction:
In today's fast-paced customer service landscape, call center agents need efficient tools to resolve issues quickly and effectively. This tutorial will guide developers in integrating Amazon Connect and Symbl.ai using Amazon Kinesis to create an AI assistant with Symbl.ai Trackers and Nebula LLM. This solution aims to provide call center agents with real-time AI assistance, enhancing their troubleshooting capabilities and improving customer satisfaction.

## Why Use Symbl.ai Over Amazon Connect's Generative AI Feature?
When comparing Symbl.ai to Amazon Connect's generative AI feature for transforming contact center experiences, there are several distinct advantages that Symbl.ai offers, particularly in terms of flexibility, depth of integration, and specialized capabilities. Here’s a detailed look at why you might choose Symbl.ai over Amazon Connect's generative AI:

**Specialized Conversational Intelligence**
Symbl.ai specializes in advanced conversational intelligence, offering capabilities that go beyond simple generative responses and real-time transcription. Its features, such as sentiment analysis, topic extraction, conversation summarization, action item detection, and follow-up tracking, provide a deeper understanding of customer interactions and enhance agent productivity. In contrast, Amazon Connect's Generative AI primarily focuses on streamlining queue selection and handling natural language inputs, making it effective for improving queue selection through natural language descriptions, but lacking the same depth of conversational analysis as Symbl.ai.

**Real-Time and Post-Conversation Insights**
With comprehensive analytics suite offerings, Symbl.ai provides both real-time and post-conversation insights, which are essential for immediate customer support and long-term strategic planning. Its real-time capabilities, including live transcription and contextual understanding, significantly enhance agent performance and customer satisfaction. Amazon Connect's Generative AI, on the other hand, primarily focuses on improving the customer interaction process during the call, particularly in queue selection, but may lack the comprehensive post-conversation insights offered by Symbl.ai, limiting its utility for ongoing improvements and strategic analysis.

**Scalability and Cross-Platform Support**
In terms of flexibility and adaptability, Symbl.ai boasts a platform-agnostic design enabling seamless integration across various communication channels such as phone, web, social media, and more, providing a consistent conversational experience across different platforms, which is ideal for businesses with diverse communication needs. In contrast, Amazon Connect's Generative AI is tightly integrated with the Amazon Connect ecosystem, offering an advantage for users deeply embedded in the AWS infrastructure, but potentially limiting its versatility when integrating with non-AWS platforms or across multiple communication channels.

**Developer and User Community Support**
Symbl.ai boasts extensive developer resources and support, facilitating easy implementation and customization according to specific requirements, alongside an active community and support forums that enable quick issue resolution and sharing of best practices. However, Amazon Connect's Generative AI, backed by the robust resources and support of AWS, is primarily focused on AWS-specific implementations, and its user community centers around AWS services, thereby limiting its exposure to broader conversational AI use cases. This makes Symbl.ai a more versatile and adaptable solution for diverse business needs.

While Amazon Connect's generative AI feature offers significant benefits for improving queue selection and customer interaction within the AWS ecosystem, Symbl.ai stands out with its specialized conversational intelligence capabilities, extensive customization options, real-time and post-conversation insights, and broader cross-platform support. For organizations looking to implement a more nuanced and flexible conversational AI solution that goes beyond the confines of queue selection, Symbl.ai presents a compelling choice.


## Why provide call center agents with AI assistance in the first place? Any stats to support this need?

In an era of rapid technological advancements, many contact centers still rely on outdated queue selection mechanisms. These traditional systems, though once effective, now fall short in delivering the efficiency and flexibility required in today's fast-paced environment. These systems struggle to adapt to fluctuating call volumes, extended wait times, inflexible routing rules which often result in calls being directed to the wrong agents, frustrating customers and agents alike.

## Why Upgrade to AI-Assisted Systems?
**1. Improved Customer Experience:**
Transitioning to AI-assisted systems in contact centers is not just a trend but a necessity. A study by Accenture found that 57% of customers are willing to switch to a competitor after just one bad experience. Embracing this technology can help contact centers stay competitive and deliver exceptional service in an increasingly demanding marketplace by offering compelling solutions that can dynamically manage queues, significantly reduce wait times for customers by analyzing caller data in real-time and ensures calls are directed to the most suitable agent, enhancing the chances of a first-call resolution.

**2. Enhanced Agent Performance:**
According to a report by Salesforce, AI can boost agent productivity by up to 40%, allowing them to handle more queries efficiently. AI tools provide agents with instant access to customer information and recommended actions, enabling faster and more accurate responses. These automated systems handle routine inquiries and tasks, freeing up agents to focus on more complex issues. 

**3. Operational Efficiency:**
AI systems require less manual setup and management, reducing the risk of errors and the need for specialized expertise. Deloitte's research indicates that AI can reduce contact center costs by up to 20% by automating routine tasks and optimizing agent performance. This automation adjusts to changing call volumes without disrupting operations.

## What Software Were Leveraged For This Solution
The software used in this solution are:
Amazon Connect: A cloud-based contact center solution that enables businesses to deliver superior customer service at a lower cost. It will be used to handle customer calls and stream audio data to Amazon Kinesis.
Amazon Kinesis: A fully managed service that makes it easy to collect, process, and analyze real-time, streaming data. It will be used to stream audio data from Amazon Connect and process it for analysis.
Symbl.ai: A conversational intelligence platform that analyzes and generates insights from natural language conversations. It will be used to transcribe and analyze audio data, set up trackers, and implement Retrieval Augmented Generation (RAG) using Nebula LLM.
Nebula LLM: A large language model that generates human-like text based on input prompts. It will be used to generate answers to customer queries based on the knowledge base and similar content.
The purpose of this software is to create an AI assistant that provides real-time assistance to call center agents, enhancing their troubleshooting capabilities and improving customer satisfaction.

## Prerequisites
You will need access to the following;

A pair of Access and Secret keys for the AWS account where Amazon Connect is configured.
A pair of appId and secret for Symbl.ai, which you can get from the platform’s main page. We use these to retrieve a temporary access token.
An API Key for Nebula LLM, which you get by joining the beta wait list.

**Set up streaming for phone conversations**
Stream data out of Amazon Connect with Amazon Kinesis

**Step 1: Set up Amazon Connect**
Create an Amazon Connect instance

**Go to the Amazon Connect dashboard.**
Click on "Create instance" and follow the on-screen instructions to set up your instance.
Configure phone numbers and routing rules

In your Amazon Connect instance, navigate to "Routing" > "Phone numbers."
Claim a new number or use an existing one, then assign it to a contact flow.
Set up routing rules by creating contact flows in "Routing" > "Contact flows."
Enable call recording and storage in Amazon S3

Go to "Analytics" > "Contact Lens" and enable it.
Enable call recording in "Routing" > "Contact flows," and configure storage in Amazon S3.
Step 2: Create an Amazon Kinesis stream
Go to the Amazon Kinesis dashboard

Navigate to the Kinesis service in the AWS Management Console.
Click on "Create stream"

```aws kinesis create-stream --stream-name MyKinesisStream --shard-count 1```

Choose "Audio" as the stream type and configure settings

Set stream type to "Audio" (if applicable).
Configure settings like stream name (MyKinesisStream) and retention period.

Step 3: Configure Amazon Connect to stream data to Kinesis
Go to the Amazon Connect dashboard

Navigate to your Amazon Connect instance.
Click on "Settings" (gear icon)

Under "Data streaming," choose "Kinesis Stream."
Configure Kinesis stream details

```aws connect associate-kinesis-video-stream \
    --instance-id <your-connect-instance-id> \
    --stream-arn <kinesis-stream-arn> \
    --role-arn <iam-role-arn>```

Enter the Kinesis stream name (MyKinesisStream) and region.
Configure additional settings like audio format and encryption.

Step 4: Test the streaming setup
Make a test call to your Amazon Connect phone number

Dial the number assigned to your Amazon Connect instance and speak for a few seconds.
Verify that the audio is being streamed to Kinesis

Use the Kinesis dashboard to view the incoming data stream.

```aws kinesis get-shard-iterator --stream-name MyKinesisStream --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON```

Step 5: Process and analyze the stream data
Use Amazon Kinesis Data Firehose to capture and process the stream data

Go to the Kinesis Data Firehose dashboard.
Create a new delivery stream and set the source to your Kinesis stream.

```aws firehose create-delivery-stream \
    --delivery-stream-name MyDeliveryStream \
    --kinesis-stream-source-configuration StreamARN=<kinesis-stream-arn>,RoleARN=<iam-role-arn>```

Apply transformations and analytics using AWS Lambda

Create a Lambda function to process the data.
```import base64
import json
import boto3

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        print("Decoded payload: " + str(payload))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }```


Configure the Kinesis stream to trigger the Lambda function.
Store the processed data in Amazon S3 or Amazon DynamoDB

Configure the Kinesis Data Firehose delivery stream to store data in S3 or DynamoDB
```aws firehose update-destination \
    --delivery-stream-name MyDeliveryStream \
    --current-delivery-stream-version-id <version-id> \
    --s3-destination-update RoleARN=<iam-role-arn>,BucketARN=<s3-bucket-arn>```

Step 6: Integrate with Symbl.ai
Get an authentication token from Symbl.ai
```
import requests
import json

url = "https://api.symbl.ai/oauth2/token:generate"
payload = {
    "type": "application",
    "appId": "38716158656e6c4a4b725a7042695a5064477447386c733235644c346d487a62",
    "appSecret": "53474e38415266727a5f76526f6e797666674645497158506342586b4c47563541494d37716f2d6a79647a32546a43745f674767334c4576755377345a795630"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
auth_token = response.json()['accessToken']
print("Auth Token:", auth_token)```


Transcribe audio for conversational intelligence
Use the Symbl.ai streaming/telephony API

Transcribe and analyze the audio data using Symbl.ai API

To generate a transcription and intelligence from both audio and text data using the Symbl.ai API, you can follow these steps:

1. Generate Access Token
First, authenticate to get the access token. This token will be used for all subsequent API calls.

Request:
```
import requests
import json

url = "https://api.symbl.ai/oauth2/token:generate"

appId = "38716158656e6c4a4b725a7042695a5064477447386c733235644c346d487a62"
appSecret = "53474e38415266727a5f76526f6e797666674645497158506342586b4c47563541494d37716f2d6a79647a32546a43745f674767334c4576755377345a795630"

payload = {
    "type": "application",
    "appId": appId,
    "appSecret": appSecret
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    access_token = response.json()['accessToken']
    print("accessToken => " + access_token)
else:
    print("Failed to get access token", response.text)```


2. Process Audio or Text Data
Now, use the access token to process your audio or text data. For this example, we will process an audio file.

Request:
```
import requests
import json

url = "https://api.symbl.ai/v1/process/audio/url"
access_token = 'your_access_token'  # Replace with the access token from the previous step

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

payload = {
  "url": "https://symbltestdata.s3.us-east-2.amazonaws.com/newPhonecall.mp3",
  "name": "Test Conversation",
  "languageCode": "en-US"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 201:
    conversation_id = response.json()['conversationId']
    job_id = response.json()['jobId']
    print("conversationId => " + conversation_id)
    print("jobId => " + job_id)
else:
    print("Failed to process audio", response.text)```



3. Check Job Status
Check the status of the job to ensure it is completed.

Request:
```
import requests

url = f'https://api.symbl.ai/v1/job/{job_id}'
access_token = 'your_access_token'

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    job_status = response.json()['status']
    print("Job Status => " + job_status)
else:
    print("Failed to get job status", response.text)```


4. Retrieve Messages with Intelligence
Finally, retrieve the messages from the conversation and include sentiment analysis.

Request:
```
import requests

base_url = "https://api.symbl.ai/v1/conversations/{conversation_id}/messages"
conversation_id = 'your_conversation_id'  # Replace with the conversationId obtained earlier
access_token = 'your_access_token'

url = base_url.format(conversation_id=conversation_id)

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

params = {
    'verbose': True, 
    'sentiment': True 
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    messages = response.json()['messages']
    for message in messages:
        print(f"Message ID: {message['id']}")
        print(f"Text: {message['text']}")
        print(f"Sentiment: {message['sentiment']['polarity']['score']}")
        print("------")
else:
    print("Failed to get messages", response.text)```


Example Response
A successful response for the messages request might look like this:
```
{
    "messages": [
        {
            "id": "5286731529191424",
            "text": "I installed your internet service for my new home and it's really slow.",
            "from": {
                "id": "36af93d9-319c-4621-911b-574ce1f7007b",
                "name": "Speaker 1"
            },
            "startTime": "2024-05-24T15:24:47.721Z",
            "endTime": "2024-05-24T15:24:50.321Z",
            "timeOffset": 5.4,
            "duration": 2.6,
            "conversationId": "6246804023803904",
            "phrases": [],
            "sentiment": {
                "polarity": {
                    "score": -0.953
                },
                "suggested": "negative"
            },
            "words": [
                {
                    "word": "I",
                    "startTime": "2024-05-24T15:24:47.721Z",
                    "endTime": "2024-05-24T15:24:48.121Z",
                    "speakerTag": 1,
                    "score": 0.87,
                    "timeOffset": 5.4,
                    "duration": 0.4
                },
                {
                    "word": "installed",
                    "startTime": "2024-05-24T15:24:48.121Z",
                    "endTime": "2024-05-24T15:24:48.221Z",
                    "speakerTag": 1,
                    "score": 0.96,
                    "timeOffset": 5.8,
                    "duration": 0.1
                },
                {
                    "word": "your",
                    "startTime": "2024-05-24T15:24:48.221Z",
                    "endTime": "2024-05-24T15:24:48.321Z",
                    "speakerTag": 1,
                    "score": 0.99,
                    "timeOffset": 5.9,
                    "duration": 0.1
                },
                {
                    "word": "internet",
                    "startTime": "2024-05-24T15:24:48.321Z",
                    "endTime": "2024-05-24T15:24:48.721Z",
                    "speakerTag": 1,
                    "score": 0.99,
                    "timeOffset": 6,
                    "duration": 0.4
                },
                {
                    "word": "service",
                    "startTime": "2024-05-24T15:24:48.721Z",
                    "endTime": "2024-05-24T15:24:49.021Z",
                    "speakerTag": 1,
                    "score": 0.99,
                    "timeOffset": 6.4,
                    "duration": 0.3
                },
                {
                    "word": "for",
                    "startTime": "2024-05-24T15:24:49.021Z",
                    "endTime": "2024-05-24T15:24:49.121Z",
                    "speakerTag": 1,
                    "score": 0.97,
                    "timeOffset": 6.7,
                    "duration": 0.1
                },
                {
                    "word": "my",
                    "startTime": "2024-05-24T15:24:49.121Z",
                    "endTime": "2024-05-24T15:24:49.321Z",
                    "speakerTag": 1,
                    "score": 1,
                    "timeOffset": 6.8,
                    "duration": 0.2
                },
                {
                    "word": "new",
                    "startTime": "2024-05-24T15:24:49.321Z",
                    "endTime": "2024-05-24T15:24:49.421Z",
                    "speakerTag": 1,
                    "score": 1,
                    "timeOffset": 7,
                    "duration": 0.1
                },
                {
                    "word": "home",
                    "startTime": "2024-05-24T15:24:49.421Z",
                    "endTime": "2024-05-24T15:24:49.621Z",
                    "speakerTag": 1,
                    "score": 1,
                    "timeOffset": 7.1,
                    "duration": 0.2
                },
                {
                    "word": "and",
                    "startTime": "2024-05-24T15:24:49.621Z",
                    "endTime": "2024-05-24T15:24:49.721Z",
                    "speakerTag": 1,
                    "score": 0.97,
                    "timeOffset": 7.3,
                    "duration": 0.1
                },
                {
                    "word": "it's",
                    "startTime": "2024-05-24T15:24:49.721Z",
                    "endTime": "2024-05-24T15:24:49.921Z",
                    "speakerTag": 1,
                    "score": 0.96,
                    "timeOffset": 7.4,
                    "duration": 0.2
                },
                {
                    "word": "really",
                    "startTime": "2024-05-24T15:24:49.921Z",
                    "endTime": "2024-05-24T15:24:50.021Z",
                    "speakerTag": 1,
                    "score": 1,
                    "timeOffset": 7.6,
                    "duration": 0.1
                },
                {
                    "word": "slow.",
                    "startTime": "2024-05-24T15:24:50.021Z",
                    "endTime": "2024-05-24T15:24:50.321Z",
                    "speakerTag": 1,
                    "score": 1,
                    "timeOffset": 7.7,
                    "duration": 0.3
                }
            ]
        }
    ]
}```



This guide provides a comprehensive overview, from setting up Amazon Connect and Kinesis to integrating with Symbl.ai for advanced conversation analytics. For detailed instructions and best practices, refer to the AWS documentation and Symbl.ai API documentation.

## Determine when call center agents receive AI assistance
To determine when call center agents receive AI assistance using Symbl.ai, you can set up trackers that use common phrases in troubleshooting calls as triggers. Here’s a detailed step-by-step guide based on your provided information:

Determine when call center agents receive AI assistance
Call center agents can receive AI assistance in various situations, such as:
Difficult customer interactions: AI can provide real-time sentiment analysis and suggest responses to de-escalate tensions.
Complex troubleshooting: AI can offer step-by-step guides and potential solutions based on similar cases.
Long call duration: AI can suggest ways to wrap up the call efficiently while ensuring customer satisfaction.
New agent training: AI can provide real-time feedback and coaching to new agents during calls.


## Set up trackers with Symbl.ai
To set up trackers with Symbl.ai, follow these steps:
Identify key phrases: Determine common phrases and keywords related to troubleshooting calls, such as "technical issue," "error message," or "product malfunction."

**Create trackers:** Use Symbl.ai's Tracker API to create custom trackers for these key phrases. This will enable real-time detection and notification when these phrases are spoken during calls.

**Configure notifications:** Set up notifications to alert agents or supervisors when a tracker is triggered. This can be done through Symbl.ai's Webhook API or integrations with other tools.

**Integrate with call center software:** Integrate Symbl.ai's trackers with your call center software to enable real-time tracking and notification during calls.

Use common phrases for troubleshooting calls as triggers
Some common phrases that can be used as triggers for AI assistance in troubleshooting calls include:
"I'm having a problem with..."
"I'm getting an error message..."
"My [product/service] is not working..."
"I've tried [solution] but it didn't work..."
"Can you help me troubleshoot...?"

When these phrases are spoken during a call, Symbl.ai's trackers can trigger AI assistance, such as:
Real-time sentiment analysis: Provide agents with sentiment analysis to understand the customer's emotional state.
Troubleshooting guides: Offer step-by-step guides and potential solutions based on similar cases.
Product information: Provide agents with relevant product information and specifications.
Solution suggestions: Suggest potential solutions based on the customer's issue.

By setting up trackers with Symbl.ai and using common phrases for troubleshooting calls as triggers, call center agents can receive timely AI assistance to resolve customer issues efficiently and effectively.


Set up trackers with Symbl.ai
Generate an Access Token: This token is required to authenticate your API requests to Symbl.ai.
```
curl -k -X POST "https://api.symbl.ai/oauth2/token:generate" \
     --header "accept: application/json" \
     --header "Content-Type: application/json" \
     -d '{
      "type" : "application",
      "appId": "YOUR_APP_ID",
      "appSecret": "YOUR_APP_SECRET"
    }'
```

Replace YOUR_APP_ID and YOUR_APP_SECRET with your actual Symbl.ai credentials. The response will include an accessToken.

Process the Audio Conversation: This involves sending the audio file to Symbl.ai for processing.
```
curl --location --request POST "https://api.symbl.ai/v1/process/audio/url" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer YOUR_ACCESS_TOKEN" \
--data-raw '{
  "url": "https://symbltestdata.s3.us-east-2.amazonaws.com/newPhonecall.mp3",
  "name": "Phone Call Analysis",
  "languageCode": "en-US"
}'
```
Replace YOUR_ACCESS_TOKEN with the token you received earlier. The response will include conversationId and jobId.

Check the Job Status: Ensure the job has been completed before proceeding.
```
curl --location --request GET "https://api.symbl.ai/v1/job/YOUR_JOB_ID" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Replace YOUR_JOB_ID with the job ID from the previous step. Wait until the job status is completed.

Set Up Trackers: Create trackers with common troubleshooting phrases as triggers.

```
curl "https://api.symbl.ai/v1/conversations/YOUR_CONVERSATION_ID/trackers" \
    --header "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    --data-raw '{
      "trackers": [
        {
          "name": "Troubleshooting",
          "vocabulary": ["restart", "reboot", "reset", "troubleshoot", "error", "not working"]
        }
      ]
    }'
```

Replace YOUR_CONVERSATION_ID with the conversation ID from the processing step. Adjust the vocabulary list with phrases relevant to your troubleshooting scenarios.

Retrieve Tracker Matches: Fetch the matches for the defined trackers to see where these phrases were used in the conversation.
```
curl "https://api.symbl.ai/v1/conversations/YOUR_CONVERSATION_ID/trackers" \
    --header "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
The response will include a list of trackers and the phrases that were matched, along with their occurrences in the conversation.

Example Scenario
After running these steps, you might get a response like this:
```
[
    {
        "id": "4712249169149952",
        "name": "Troubleshooting",
        "matches": [
            {
                "type": "vocabulary",
                "value": "restart",
                "messageRefs": [
                    {
                        "id": "5192198242041856",
                        "text": "Can you please restart your device?",
                        "offset": -1
                    }
                ],
                "insightRefs": []
            },
            {
                "type": "vocabulary",
                "value": "error",
                "messageRefs": [
                    {
                        "id": "5613607799881728",
                        "text": "Are you seeing any error messages?",
                        "offset": -1
                    }
                ],
                "insightRefs": []
            }
        ]
    }
]
```

This output indicates that the phrases "restart" and "error" were used during the call, triggering the "Troubleshooting" tracker. Using this information, you can identify specific points in the call where the agent provided troubleshooting assistance.



Here is a step-by-step guide to building a real-time agent assist chatbot using Nebula LLM and RAG with a Python SDK:

Step 1: Install Python SDK
Install the Symbl AI Python SDK using pip: pip install symbl-ai

Step 2: Set up API Access
Import the SDK and set up API access using your AppId and AppSecret:

from symbl_ai import Symbl

symbl = Symbl(app_id='YOUR_APP_ID', app_secret='YOUR_APP_SECRET')
