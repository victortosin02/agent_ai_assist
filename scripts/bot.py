import torch
from transformers import BartForConditionalGeneration, BartTokenizer
from elasticsearch import Elasticsearch
import requests
import json

# Initialize Elasticsearch client
es = Elasticsearch()

# Initialize BART model and tokenizer
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

# Symbl.ai API key and URL
SYMBL_API_KEY = 'YOUR_SYMBL_API_KEY'
SYMBL_URL_TRACKER = 'https://api.symbl.ai/v1/process/text'

def symbl_extract_context(query):
    headers = {
        'Authorization': f'Bearer {SYMBL_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'messages': [{'payload': {'content': query, 'contentType': 'text/plain'}}]
    }
    response = requests.post(SYMBL_URL_TRACKER, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    # Extract key phrases and topics from Symbl.ai response
    key_phrases = [phrase['text'] for phrase in response_data.get('context', {}).get('keyPhrases', [])]
    topics = [topic['text'] for topic in response_data.get('context', {}).get('topics', [])]
    
    # Extract matched phrases from tracker
    trackers = response_data.get('trackers', {}).get('matches', [])
    matched_phrases = [match['text'] for match in trackers]

    # Combine key phrases, topics, and matched phrases for enhanced retrieval
    context_terms = key_phrases + topics + matched_phrases
    return ' '.join(context_terms)

def retrieve_training_materials(query):
    # Enhance query with context extraction using Symbl.ai
    enhanced_query = symbl_extract_context(query)
    
    # Search for relevant documents in Elasticsearch
    search_response = es.search(index='knowledge_base', body={'query': {'match': {'content': enhanced_query}}})
    relevant_docs = [hit['_source']['content'] for hit in search_response['hits']['hits']]
    return relevant_docs

def generate_response(query, context):
    # Combine the query with retrieved context
    combined_input = query + " " + " ".join(context)
    
    # Tokenize the combined input
    input_ids = tokenizer.encode(combined_input, return_tensors='pt', truncation=True, max_length=1024)
    
    # Generate the response
    output = model.generate(input_ids=input_ids, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return response

def rag(query):
    # Retrieve relevant documents
    relevant_docs = retrieve_training_materials(query)
    
    # Generate response with context
    response = generate_response(query, relevant_docs)
    
    return response

# Test the RAG model
query = 'How do I troubleshoot a slow computer?'
response = rag(query)
print(response)


# Main function to run the chatbot
def main():
    print("Welcome to the Agent Assist Chatbot!")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        response = rag(user_query)
        print(f"Bot: {response}")

# Run the chatbot
if __name__ == "__main__":
    main()