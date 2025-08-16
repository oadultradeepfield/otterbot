# Otterbot

Otterbot is a Python Telegram bot template that sends daily task reminders from Google Sheets using the Google Sheets
API. The bot runs on a schedule through GitHub Actions.

The main benefit of this approach is that it's completely serverless with zero hosting costs. The downside is that you
cannot interact with the bot in real-time. If you only need basic functionality, this repository is essentially
plug-and-play—you can configure it using the steps below and start using it without any coding.

## Basic Setup

### Telegram Setup

1. Create your bot using [@BotFather](https://telegram.me/BotFather) and customize its personality. There are many good
   tutorials online for this step.
2. After creating the bot, copy the `TELEGRAM_BOT_TOKEN` and add it to your GitHub repository secrets under Settings >
   Secrets and variables > Actions.
3. Send a message to your bot to initiate contact, then use a tool like [@userinfobot](https://telegram.me/userinfobot)
   to get your chat ID. Add this as `TELEGRAM_CHAT_ID` in your repository secrets.

### Google Cloud Setup

1. Create a new Google Cloud project or use an existing one.
2. Enable the Google Sheets API by going to APIs & Services > Library and searching for "Google Sheets API".
3. Go to APIs & Services > Credentials and create a service account. You can skip the permission settings for now.
4. Download the JSON credentials file for the service account, then paste its entire content as
   `GOOGLE_SHEETS_CREDENTIALS` in your repository secrets.

### Google Sheet Setup

1. Create a Google Sheet with the following three columns:

   | name   | date       | estimated_hours |
      |--------|------------|-----------------|
   | Task 1 | 2025-07-16 | 2.5             |

   **Note:** The `date` must be in `YYYY-MM-DD` format. The `estimated_hours` should be a number (can include decimals)
   representing the hours you estimate to spend on the task.

2. Share your Google Sheet with the service account's client email address (found in the JSON credentials). Read-only
   access is sufficient.

3. Extract the spreadsheet ID from your Google Sheet URL. For example, in the URL
   `https://docs.google.com/spreadsheets/d/abc1234567/edit#gid=0`, the spreadsheet ID is `abc1234567`. Add this as the
   secret `GOOGLE_SHEETS_SHEET_ID`.

4. Copy the full URL of your Google Sheet and add it as the secret `GOOGLE_SHEETS_SHEET_LINK`. This will be included in
   reminder messages for easy access to your sheet.

Once you've completed these steps, you can start using your forked version of OtterBot with your own customizations. You
can modify the bot's personality by editing the text strings in the Python files.

## Local Development

### Prerequisites

1. Ensure you have Python 3.9+ installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Testing

1. Create a `.env` file in the project root with all the environment variables mentioned above.
2. Run the task scheduler to test the daily reminder functionality:
   ```bash
   python task_scheduler.py
   ```
3. If you make changes to the GitHub Actions workflow, you can use the manual trigger dispatch action to test without
   waiting for the scheduled run.

## License

This project is licensed under the MIT License. See [LICENSE](/LICENSE) for more details.