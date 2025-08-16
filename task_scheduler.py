import os
from datetime import datetime

from dotenv import load_dotenv

from google_sheets_manager import GoogleSheetsManager
from telegram_sender import format_daily_tasks, send_telegram_messages


def run_daily_reminder():
    """Main function for running daily reminder"""
    print("🦦 OtterBot starting daily reminder...")

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Checking tasks for: {today}")

    # Initialize data manager
    try:
        data_manager = GoogleSheetsManager()
        tasks = data_manager.get_tasks_for_date(today)
        print(f"Found {len(tasks)} tasks for today")

        # Format message
        message = format_daily_tasks(tasks)

        # Send to user
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            print("Error: TELEGRAM_CHAT_ID not set")
            return

        success = send_telegram_messages(chat_id, message)
        if success:
            print("✅ Daily reminder sent successfully!")
        else:
            print("❌ Failed to send daily reminder")

    except Exception as e:
        print(f"Error in daily reminder: {e}")


if __name__ == "__main__":
    load_dotenv()
    run_daily_reminder()
