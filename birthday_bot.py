import csv
import os
from dateutil import parser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from datetime import datetime

# ===== CONFIG =====
TEST_MODE = False             # Use test date instead of today's real date
TEST_DATE = "10-20"          # Change this for testing birthdays
TEST_MESSAGE = False          # True = send test message, False = send real message

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
channel_id = os.getenv("CHANNEL_ID")

def get_birthdays_today():
    today = TEST_DATE if TEST_MODE else datetime.today().strftime("%m-%d")
    birthdays_today = []

    with open("birthdays.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row["birthday"]:
                continue
            try:
                date_obj = parser.parse(row["birthday"], fuzzy=True, dayfirst=False)
                bday_mm_dd = date_obj.strftime("%m-%d")
                if bday_mm_dd == today:
                    birthdays_today.append(row)
            except Exception as e:
                print(f"⚠️ Could not parse date for {row['name']}: {row['birthday']} ({e})")
    return birthdays_today

def get_user_profile_image(user_id):
    try:
        response = client.users_profile_get(user=user_id)
        image_url = response["profile"].get("image_512")
        return image_url
    except Exception as e:
        print(f"Error getting profile image for {user_id}: {e}")
        return None

def send_birthday_message(user_id, name):
    if TEST_MESSAGE:
        # Test message (no profile picture)
        text = (
            f"🛠️ (TEST) Birthday Bot is working!\n\n"
            f":tada: Happy Birthday <@{user_id}>! :tada:\n\n"
            f"Wishing you a year filled with bold ideas, big wins, and all the good vibes! "
            f"Your brilliance lights up the team, today we celebrate you! :partying_face: "
            f"Let’s make this next chapter your best one yet :rocket:"
        )
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text}
            }
        ]
    else:
        # Real birthday message (with optional profile picture)
        text = (
            f":tada: Happy Birthday <@{user_id}>! :tada:\n\n"
            f"Wishing you a year filled with bold ideas, big wins, and all the good vibes! "
            f"Your brilliance lights up the team, today we celebrate you! :partying_face: "
            f"Let’s make this next chapter your best one yet :rocket:"
        )

        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text}
            }
        ]

        image_url = get_user_profile_image(user_id)
        if image_url:
            blocks.append(
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": f"{name}'s profile picture"
                }
            )

    try:
        client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            text="(TEST) Birthday Bot" if TEST_MESSAGE else f"Happy Birthday {name}!"
        )
        print(f"✅ Sent {'test ' if TEST_MESSAGE else ''}message to {name}")
    except SlackApiError as e:
        print(f"❌ Error sending message to {name}: {e.response['error']}")

if __name__ == "__main__":
    birthdays = get_birthdays_today()
    if birthdays:
        print("🎉 Today's birthdays:")
        for person in birthdays:
            print(f"- {person['name']} ({person['birthday']}) - Slack ID: {person['user_id']}")
            send_birthday_message(person['user_id'], person['name'])
    else:
        print("No birthdays today.")


