# Tests api google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.functions import *
from src.utils.dummies import *

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "token.json",
    scope,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore
sheet_name = "API"
spreadsheet = client.open(sheet_name)

sheet = spreadsheet.get_worksheet(1)
data = sheet.get_all_values()

all_merges = get_all_merges(sheet)


merge = all_merges[3]

for merge in all_merges:
    print(get_text_from_merged_cell(data, merge))
