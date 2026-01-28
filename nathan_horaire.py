# Tests api google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "nathan-petitboulanger-1b097cac714e.json",
    scope,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore


sheet_name = "API"
spreadsheet = client.open(sheet_name)
sheet = spreadsheet.sheet1  # Accède au premier onglet


data = sheet.get_all_values()

meta_data = spreadsheet.fetch_sheet_metadata()
merges = meta_data["sheets"][0]["merges"]
merges_lundi = [merge for merge in merges if merge["startColumnIndex"] == 1]

id_col_horaire = 0
for merge in merges_lundi:
    start_row_id = merge["startRowIndex"]
    end_row_id = merge["endRowIndex"] - 1
    col_id = merge["startColumnIndex"]
    content = data[start_row_id][col_id]
    start_h = data[start_row_id][id_col_horaire]
    end_h = data[end_row_id][id_col_horaire]
    print(f" la phase {content} commence à {start_h}h et fini à {int(end_h) + 1}h")
