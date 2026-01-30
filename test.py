# Tests api google sheet
import re
import dateparser
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from utils.functions import *
from utils.dummies import *

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

metadata = spreadsheet.fetch_sheet_metadata()


sheet = spreadsheet.get_worksheet(4)

start_row, start_col = 2, 2
end_row, end_col = 5, 2


sheet.merge_cells(start_row, start_col, end_row, end_col)

sheet.unmerge_cells(start_row, start_col, end_row, end_col)

sheet.update_cell(2, 2, "Cours de SIG - Marc Lang")


import gspread
from gspread_formatting import (
    get_user_entered_format,
    CellFormat,
    TextFormat,
    Color,
    batch_updater,
    format_cell_range,
)


mon_format_complet = CellFormat(
    backgroundColor=Color(1, 0, 0.9),  # Gris clair
    textFormat=TextFormat(bold=True, foregroundColor=Color(1, 0, 0)),
    horizontalAlignment="CENTER",  # Centré
)

with batch_updater(spreadsheet) as batch:
    batch.format_cell_range(sheet, "A1:Z100", mon_format_complet)
    batch.format_cell_range(sheet, "C10:C12", mon_format_complet)


def get_color_cours_mapping():
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
    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)
    sheet = spreadsheet.get_worksheet(1)

    color_cours = {}
    cell = sheet.find("QEGR")
    data = sheet.get_all_values()

    row_id = cell.row - 1
    col_id = cell.col - 1
    while data[row_id][col_id] != "":
        print(data[row_id][col_id])
        color_cours[data[row_id][col_id]] = extract_rgb_from_cell_coords(
            metadata, row_id, col_id
        )
        row_id += 1
        col_id

    return color_cours


get_color_cours_mapping()

extract_rgb_from_cell_coords(metadata, 1, 14)
