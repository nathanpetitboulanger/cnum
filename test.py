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

all_merges = get_all_merges(spreadsheet)
