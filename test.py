# Tests api google sheet
import re
import dateparser
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from utils.functions import *
from utils.dummies import *
import pandas as pd
import dateparser
from babel.dates import format_date, format_time

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


sheet = spreadsheet.get_worksheet(1)

data = sheet.get_all_values()

df = pd.read_csv("final.csv").drop("Unnamed: 0", axis=1)

df["start"] = pd.to_datetime(df["start"])

df["end"] = pd.to_datetime(df["end"])
df = df.sort_values("delta", ascending=False)

start = df.iloc[0]["start"]
end = df.iloc[0]["end"]

index_sheet = get_index_sheet(sheet)


best_idx_start_relative, best_idx_end_relative, index_row_date = (
    get_best_index_from_delta(start, end, index_sheet, data)
)

print(best_idx_start_relative, best_idx_end_relative, index_row_date)


sheet = spreadsheet.get_worksheet(4)
sheet

start_row_index = 2
end_row_index = 10
sheet_id = 5

requests = []


requests.append(
    {
        "mergeCells": {
            "range": {
                "sheetId": sheet.id,
                "startRowIndex": start_row_index,
                "endRowIndex": end_row_index,
                "startColumnIndex": 0,
                "endColumnIndex": 2,
            },
            "mergeType": "MERGE_ALL",
        }
    }
)

# Envoi de toutes les demandes en une seule fois
spreadsheet.batch_update({"requests": requests})


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

    creds = serviceaccountcredentials.from_json_keyfile_name(
        "token.json",
        scope,  # type: ignore
    )

    client = gspread.authorize(creds)  # type: ignore
    sheet_name = "api"
    spreadsheet = client.open(sheet_name)
    params = {
        "includegriddata": true,
        "fields": "sheets(data(rowdata(values(effectiveformat(backgroundcolorstyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)
    sheet = spreadsheet.get_worksheet(1)

    color_cours = {}
    cell = sheet.find("qegr")
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


extract_rgb_from_cell_coords(metadata, 1, 14)
