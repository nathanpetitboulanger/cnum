import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from typing import Mapping

from config import (
    CREDENTIALS_FILE,
    DEFAULT_SPREADSHEET_NAME,
    SCOPES,
    edt_sheet_index,
)
from pyasn1_modules.rfc5208 import sha1WithRSAEncryption
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


def get_df_from_sheet_name(sheet_name: str = "edt_clean"):
    """
    Returns a pandas DataFrame of a clean_worksheet by its name.
    Automatically parses 'start' and 'end' columns as datetimes.
    """
    spreadsheet = get_spreadsheet()
    sheet = spreadsheet.worksheet(sheet_name)
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


def extract_legend(
    meta_data: Mapping,
    sheet_param: gspread.Worksheet,
):
    data = sheet_param.get_all_values()
    col_nom = 0
    actual_row = 2
    col_color = 1

    color_mapping = {}

    while True:
        try:
            color = extract_rgb_from_cell_coords(meta_data, actual_row, col_color, 0)

        except KeyError:
            color = (1, 1, 1)

        if color == (1, 1, 1):
            break

        nom_cellule = data[actual_row][col_nom]
        color_mapping[nom_cellule] = color
        actual_row += 1

    color_mapping_reversed = {couleur: nom for nom, couleur in color_mapping.items()}

    return color_mapping_reversed


def extract_name_from_code(data: list[list]):
    """
    need data from params sheet
    """
    col_code = 3
    actual_row = 1
    col_teacher = 4
    teacher_code = {}

    while True:
        name = data[actual_row][col_teacher]

        if name is None or str(name).strip() == "":
            break

        name_cell = data[actual_row][col_code]
        teacher_code[name_cell] = name
        actual_row += 1

    return teacher_code


def get_mapping_dict_for_name(spreadsheet):
    sheet = spreadsheet.worksheet("Paramètres")  # type: ignore
    data_params = sheet.get_all_values()
    names_codes = extract_name_from_code(data_params)

    coodes_names = pd.Series(names_codes)
    return coodes_names
