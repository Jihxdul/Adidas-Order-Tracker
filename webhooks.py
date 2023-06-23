import requests
import json

def send_discord_webhook(webhook_url,embed):
    data = {
        "embeds": [embed],
        "content": ""
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        print("Webhook message sent successfully!")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")

