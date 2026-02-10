import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from config import (
    CREDENTIALS_FILE,
    DEFAULT_SPREADSHEET_NAME,
    SCOPES,
    edt_sheet_index,
)
from utils.functions import extract_rgb_from_cell_coords


def get_gspread_client():
    """Authenticates and returns a gspread client."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )
    return gspread.authorize(creds)


def get_spreadsheet(name=DEFAULT_SPREADSHEET_NAME):
    """Opens and returns a gspread spreadsheet."""
    client = get_gspread_client()
    return client.open(name)


def get_color_cours_mapping():
    """
    Returns a dictionary mapping course names to their RGB color.
    Iterates from the 'QEGR' cell downwards until an empty cell is found.
    """
    spreadsheet = get_spreadsheet()

    # Fetch formatting metadata for all cells
    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)

    # Use the worksheet specified in config
    sheet = spreadsheet.get_worksheet(edt_sheet_index)
    data = sheet.get_all_values()

    try:
        cell_qegr = sheet.find("QEGR")
    except gspread.exceptions.CellNotFound:
        print("Warning: Cell 'QEGR' not found in the worksheet.")
        return {}

    color_cours = {}
    row_idx = cell_qegr.row - 1
    col_idx = cell_qegr.col - 1

    # Traverse downwards and extract colors for each course
    while row_idx < len(data) and data[row_idx][col_idx]:
        course_name = data[row_idx][col_idx]
        print(f"Processing: {course_name}")

        color_cours[course_name] = extract_rgb_from_cell_coords(
            metadata, row_idx, col_idx, sheet_id=edt_sheet_index
        )
        row_idx += 1

    return color_cours


def get_df_from_sheet_index(sheet_index: int):
    """
    Returns a pandas DataFrame of a clean_worksheet by its index.
    Automatically parses 'start' and 'end' columns as datetimes.
    """
    spreadsheet = get_spreadsheet()
    sheet = spreadsheet.get_worksheet(sheet_index)
    data = sheet.get_all_values()

    if not data:
        return pd.DataFrame()

    # Create DataFrame using the first row as columns
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # Convert date columns if they exist
    for date_col in ["start", "end"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])

    return df
