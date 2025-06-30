import os
import json
import gspread
from google.oauth2.service_account import Credentials
from app.config import settings

class GoogleSheetsClient:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds_dict = json.loads(os.environ["GSPREAD_CREDENTIALS_JSON"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        self.client = gspread.authorize(creds)

    def get_sheet_data(self):
        sheet = self.client.open(settings.SHEET_NAME).worksheet(settings.WORKSHEET_NAME)
        return sheet.get_all_records()

    def batch_update_rows(self, updates):
        pass  # Optional: can be implemented later
