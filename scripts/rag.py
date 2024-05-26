import symbl

# START changing values here.

app_id = "<APP_ID>"
app_secret = "<APP_SECRET>"
phone_number = "<PHONE_NUMBER>"
email = "<EMAIL>"
knowledge_base = "<KNOWLEDGE_BASE>"  # Add your knowledge base documents here
conversation_id = "<CONVERSATION_ID>"  # Replace with your conversation ID
access_token = "<ACCESS_TOKEN>"  # Replace with your access token

# STOP changing values here.

# Set up API access
symbl = symbl.Symbl(app_id=app_id, app_secret=app_secret)

# Index knowledge base using Nebula Embedding API
embeddings = symbl.embedding(text=knowledge_base)

# Set up trackers using Symbl AI platform
trackers = [
    {
        "name": "Troubleshooting",
        "vocabulary": ["restart", "reboot", "reset", "troubleshoot", "error", "not working"]
    }
]
symbl.create_trackers(conversation_id, trackers, access_token)

# Stream conversations using Web SDK
connection_object = symbl.Telephony.start_pstn(
    credentials={"app_id": app_id, "app_secret": app_secret},
    phone_number=phone_number,
    actions=[
        {
            "invokeOn": "stop",
            "name": "sendSummaryEmail",
            "parameters": {
                "emails": [
                    email
                ],
            },
        },
    ]
)

# Implement RAG using Nebula LLM
def generate_answer(trigger):
    # Vectorize trigger using Nebula Embedding API
    trigger_embedding = symbl.embedding(text=trigger)
    
    # Query vector database to identify similar vectors and associated content
    similar_embeddings = symbl.query_vector_database(trigger_embedding, embeddings)
    
    # Use Nebula LLM to generate answer based on similar content
    answer = symbl.generate_answer(similar_embeddings, knowledge_base)
    
    return answer

# Set up agent assist chatbot
def agent_assist_chatbot():
    while True:
        customer_query = input("Customer Query: ")
        agent_response = generate_answer(customer_query)
        print("Agent Response:", agent_response)

# Run chatbot
agent_assist_chatbot()