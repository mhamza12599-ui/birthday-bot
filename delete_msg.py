import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN") or "xoxb-your-bot-token"
CHANNEL_ID = "C091S15JB42"
TS = "1762656371.319069"

client = WebClient(token=SLACK_BOT_TOKEN)

try:
    resp = client.chat_delete(channel=CHANNEL_ID, ts=TS)
    print("Deleted:", resp.get("ok", False))
except SlackApiError as e:
    print("Error:", e.response.get("error"))
