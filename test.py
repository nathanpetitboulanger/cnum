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
from babel.dates import format_date

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



start = df.iloc[1]["start"]
end = df.iloc[1]["end"]


start_date_str = format_date(start, format="full", locale="fr_FR")
end_date_str = format_date(end, format="full", locale="fr_FR")


start_hour_str = format_date(start, format="full", locale="fr_FR")
end_hour_str = format_date(end, format="full", locale="fr_FR")





index_sheet = get_index_sheet(sheet)

index_date = index_sheet.get(end_hour_str, [None])[0]

row_date = index_date[0]

times_rows = data[row_date:row_date + 8]

times =  [time[0] for time in times_rows]







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
