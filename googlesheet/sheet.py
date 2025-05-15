import gspread
import os

from google.oauth2.service_account import Credentials

from utils.references import References

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds_file = os.path.join(References.FOLDER_DATAS, "bfrl_credentials.json")
assert os.path.exists(creds_file), f"{creds_file} don't exist"
creds = Credentials.from_service_account_file(creds_file, scopes=scopes)

sheet_client = gspread.authorize(creds)
sheet = sheet_client.open_by_key(References.SHEET_ID)

global_worksheet = sheet.get_worksheet(0)
normal_worksheet = sheet.get_worksheet(1)
short_worksheet = sheet.get_worksheet(2)
extrashort_worksheet = sheet.get_worksheet(3)