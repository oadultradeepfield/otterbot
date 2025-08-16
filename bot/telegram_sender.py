import os
from typing import Dict, List

import requests


def send_telegram_messages(chat_id: str, message: str) -> bool:
    """Send message via Telegram API."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise EnvironmentError("TELEGRAM_BOT_TOKEN is not set")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {e}")
        return False


def format_daily_tasks(tasks: List[Dict]) -> str:
    """Format daily tasks into friendly OtterBot message."""
    if not tasks:
        return "🦦 *Good morning!* No tasks scheduled for today. Time to relax! 🌊"

    total_hours = sum(task.get("estimated_hours", 0) for task in tasks)
    message = f"🦦 *Good morning! Here are your tasks for today:*\n\n"

    for i, task in enumerate(tasks, 1):
        hours = task.get("estimated_hours", 0)
        hours_text = f" ({hours}h)" if hours > 0 else ""
        message += f"{i}. *{task['name']}*{hours_text}\n"

    message += f"\n⏱ Total estimated time: *{total_hours} hours*"
    message += f"\n🌊 You've got this! Stay focused like an otter hunting fish! 🐟"
    return message
