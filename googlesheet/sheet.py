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

values = sheet.sheet1.row_values(1)
print(values)