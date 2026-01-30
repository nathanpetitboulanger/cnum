# Tests api google sheet
import re
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

merge = all_merges[0]

params = {
    "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))"
}
metadata = spreadsheet.fetch_sheet_metadata(params=params)
sheet_data = metadata["sheets"][1]["data"][0]
row_data = sheet_data.get("rowData", [])


row = 6
col = 1


def get_head_cell_coords_from_merge(merge):
    row_id = merge["startRowIndex"]
    col_id = merge["startColumnIndex"]
    return row_id, col_id


def extract_rgb_from_cell_coords(metadata, row, col):
    sheet_data = metadata["sheets"][1]["data"][0]
    row_data = sheet_data.get("rowData", [])

    cell_values = row_data[row]["values"][col]
    rgb = cell_values["effectiveFormat"]["backgroundColorStyle"]["rgbColor"]
    return (rgb.get("red", 0), rgb.get("green", 0), rgb.get("blue", 0))


def extract_rgb_form_merge(metadata, merge):
    row_id, col_id = get_head_cell_coords_from_merge(merge)
    return extract_rgb_from_cell_coords(metadata, row_id, col_id)


extract_rgb_form_merge(metadata, merge)
