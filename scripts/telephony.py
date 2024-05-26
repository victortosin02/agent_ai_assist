import symbl

# START changing values here.

app_id = "<APP_ID>"
app_secret = "<APP_SECRET>"
phone_number = "<PHONE_NUMBER>"
email = "<EMAIL>"

# STOP changing values here.

connection_object = symbl.Telephony.start_pstn(
  credentials={"app_id": app_id, "app_secret": app_secret},
  phone_number=phone_number,
  actions = [
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

print("Conversation ID: " + connection_object.conversation.get_conversation_id())