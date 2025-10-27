import json
import os
from typing import Dict, List

import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


class GoogleSheetsManager:
    def __init__(self):
        # Load service account credentials from environment
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        if not creds_json:
            raise EnvironmentError("GOOGLE_SHEETS_CREDENTIALS is not set")

        sheet_id = os.getenv("GOOGLE_SHEETS_SHEET_ID")
        if not sheet_id:
            raise EnvironmentError("GOOGLE_SHEETS_SHEET_ID is not set")

        creds_dict = json.loads(creds_json)
        self.credentials = Credentials.from_service_account_info(
            creds_dict, scopes=SCOPES
        )
        self.client = gspread.authorize(self.credentials)
        self.sheet_id = sheet_id

    def get_tasks_for_date(self, date_str: str) -> List[Dict]:
        """Get all tasks for a specific date (YYYY-MM-DD format)"""
        try:
            sheet = self.client.open_by_key(self.sheet_id).sheet1
            records = sheet.get_all_records()

            tasks = []
            for record in records:
                task_date = record.get("date", "").strip()
                if task_date == date_str and record.get("name", "").strip():
                    tasks.append(
                        {
                            "name": record["name"].strip(),
                            "date": task_date,
                            "estimated_hours": parse_hours(
                                record.get("estimated_hours", "")
                            ),
                        }
                    )

            return tasks
        except Exception as e:
            print(f"Error reading Google Sheets: {e}")
            return []


def parse_hours(hours_value) -> float:
    """Parse hours value from sheet (handles both string and numeric)"""
    try:
        hours = float(hours_value) if hours_value else 0
        return max(0, hours)
    except (ValueError, TypeError):
        return 0
