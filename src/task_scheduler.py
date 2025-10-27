import json
import os
from datetime import datetime
from hashlib import md5

from dotenv import load_dotenv

from google_sheets_manager import GoogleSheetsManager
from telegram_sender import format_daily_tasks, send_telegram_messages

LAST_MESSAGE_HASH_FILE = ".last_message_hash"


def get_last_message_hash():
    """Retrieve the hash of the last sent message"""
    if os.path.exists(LAST_MESSAGE_HASH_FILE):
        try:
            with open(LAST_MESSAGE_HASH_FILE, "r") as f:
                data = json.load(f)
                return data.get("hash")
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_message_hash(message_hash):
    """Save the hash with timestamp"""
    with open(LAST_MESSAGE_HASH_FILE, "w") as f:
        json.dump({"hash": message_hash, "timestamp": datetime.now().isoformat()}, f)


def calculate_message_hash(message):
    """Calculate MD5 hash of the message"""
    return md5(message.encode()).hexdigest()


def run_reminder():
    """Main function for running task reminder"""
    print("🦦 OtterBot starting sending reminder...")

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Checking tasks for: {today}")

    try:
        data_manager = GoogleSheetsManager()
        tasks = data_manager.get_tasks_for_date(today)
        message = format_daily_tasks(tasks)

        current_hash = calculate_message_hash(message)
        last_hash = get_last_message_hash()

        if current_hash == last_hash:
            print("⏭️ No changes in tasks, skipping reminder")
            return

        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            print("Error: TELEGRAM_CHAT_ID not set")
            return

        success = send_telegram_messages(chat_id, message)
        if success:
            print("✅ Daily reminder sent successfully!")
            save_message_hash(current_hash)
        else:
            print("❌ Failed to send daily reminder")

    except Exception as e:
        print(f"Error in daily reminder: {e}")


if __name__ == "__main__":
    load_dotenv()
    run_reminder()
