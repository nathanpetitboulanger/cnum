# Tests api google sheet
import dateparser
import gspread
from datetime import datetime
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

data
merge = {
    "sheetId": 739511890,
    "startRowIndex": 6,
    "endRowIndex": 10,
    "startColumnIndex": 3,
}

merge = {
    "sheetId": 739511890,
    "startRowIndex": 70,
    "endRowIndex": 72,
    "startColumnIndex": 11,
    "endColumnIndex": 12,
}


cours = []
for merge in all_merges:
    print(merge)
    try:
        delta = get_time_delta_from_merge(data, merge)
        str_cours = get_text_from_merged_cell(data, merge)
        cours.append([str_cours, delta, merge])
    except Exception as e:
        print(e)
        pass


len(cours)
