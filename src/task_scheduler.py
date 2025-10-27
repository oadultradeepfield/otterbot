import os
from datetime import datetime

from dotenv import load_dotenv

from src.google_sheets_manager import GoogleSheetsManager
from src.telegram_sender import format_daily_tasks, send_telegram_messages


def run_reminder():
    """Main function for running task reminder"""
    print("🦦 OtterBot starting sending reminder...")

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Checking tasks for: {today}")

    # Initialize data manager
    try:
        data_manager = GoogleSheetsManager()
        tasks = data_manager.get_tasks_for_date(today)
        message = format_daily_tasks(tasks)

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
    run_reminder()
