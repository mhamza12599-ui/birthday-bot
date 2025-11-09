import csv
import os
from slack_sdk import WebClient

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=SLACK_BOT_TOKEN)

def fetch_slack_users():
    users_list = []
    cursor = None

    while True:
        response = client.users_list(cursor=cursor)
        members = response.get("members", [])

        for member in members:
            if member.get("is_bot") or member.get("deleted"):
                continue

            users_list.append({
                "user_id": member["id"],
                "name": member["profile"].get("real_name_normalized", ""),
                "display_name": member["profile"].get("display_name", "")
            })

        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return users_list

if __name__ == "__main__":
    users = fetch_slack_users()

    with open("slack_users.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "display_name"])
        writer.writeheader()
        writer.writerows(users)

    print("✅ Slack user list saved to slack_users.csv!")
