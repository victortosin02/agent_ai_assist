import requests

app_id = "\<APP_ID>"        # Replace with your App ID  
app_secret = "\<APP_SECRET>" # Replace with your App Secret

url = "https://api.symbl.ai/oauth2/token:generate" 
headers = {"Content-Type": "application/json"}  
data = {"type": "application", "appId": app_id, "appSecret": app_secret}

response = requests.post(url, headers=headers, json=data)  
access_token = response.json()["accessToken"]