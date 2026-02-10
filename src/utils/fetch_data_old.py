from oauth2client.service_account import ServiceAccountCredentials
from utils.functions import extract_rgb_from_cell_coords
import gspread
import pandas as pd
from config import CREDENTIALS_FILE, SCOPES, DEFAULT_SPREADSHEET_NAME, edt_sheet_index


def get_color_cours_mapping():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )

    client = gspread.authorize(creds)  # type: ignore
    spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)
    sheet = spreadsheet.get_worksheet(edt_sheet_index)

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


def get_df_from_sheet_index(sheet_index: int):
    """
    return the df of a clean_worksheet
    """

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )

    client = gspread.authorize(creds)  # type: ignore
    spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
    sheet = spreadsheet.get_worksheet(sheet_index)
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0:1][0])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df
