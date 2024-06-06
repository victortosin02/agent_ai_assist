import requests

app_id = "38716158656e6c4a4b725a7042695a5064477447386c733235644c346d487a62"
app_secret = "53474e38415266727a5f76526f6e797666674645497158506342586b4c47563541494d37716f2d6a79647a32546a43745f674767334c4576755377345a795630"

url = "https://api.symbl.ai/oauth2/token:generate"

headers = {
  "Content-Type": "application/json"
}

request_body = {
  "type": "application",
  "appId": app_id,
  "appSecret": app_secret
}

response = requests.post(url, headers=headers, json=request_body)

print(response.json())