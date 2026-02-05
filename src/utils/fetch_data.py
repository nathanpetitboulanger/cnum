from oauth2client.service_account import ServiceAccountCredentials
from utils.functions import extract_rgb_from_cell_coords
import gspread
import pandas as pd


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


def get_df():
    df = pd.read_csv("finale.csv").drop("Unnamed: 0", axis=1)
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df
