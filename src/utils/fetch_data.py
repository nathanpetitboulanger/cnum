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


def get_color_cours_mapping(spreadsheet):
    """
    Returns a dictionary mapping course names to their RGB color.
    Iterates from the 'QEGR' cell downwards until an empty cell is found.
    """

    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)

    sheet = spreadsheet.worksheet("EDT")
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
    sheet = spreadsheet.worksheet("EDT")
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


df = get_df_from_sheet_name()


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
            color = extract_rgb_from_cell_coords(
                meta_data, actual_row, col_color, sheet_id=0
            )

        except KeyError:
            color = (1, 1, 1)

        if color == (1, 1, 1):
            break

        nom_cellule = data[actual_row][col_nom]
        color_mapping[nom_cellule] = color
        actual_row += 1
        print(actual_row)

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
    """
    return the mapping dict in Paramètres sheet
    """
    sheet = spreadsheet.worksheet("Paramètres")  # type: ignore
    data_params = sheet.get_all_values()
    names_codes = extract_name_from_code(data_params)

    coodes_names = pd.Series(names_codes)
    return coodes_names


def get_mapping_dict_for_group_color(spreadsheet):
    """
    Returns a dictionary mapping group names to their RGB color in the 'Paramètres' sheet.
    Detects the 'Groupe' cell and iterates downwards.
    """
    sheet = spreadsheet.worksheet("Paramètres")
    data_params = sheet.get_all_values()

    # 1. Fetch metadata for colors
    params = {
        "includeGridData": True,
        "fields": "sheets(properties(title,sheetId),data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)

    # 2. Find the correct sheet metadata index
    sheet_meta_idx = None
    for idx, s in enumerate(metadata["sheets"]):
        if s["properties"]["title"] == "Paramètres":
            sheet_meta_idx = idx
            break

    if sheet_meta_idx is None:
        return {}

    # 3. Find 'Groupe' position in data
    row_groupe = -1
    col_groupe = -1
    for r, row in enumerate(data_params):
        for c, val in enumerate(row):
            if val == "Groupes":
                row_groupe = r
                col_groupe = c
                break
        if row_groupe != -1:
            break

    if row_groupe == -1:
        print("Warning: Cell 'Groupes' not found in 'Paramètres'.")
        return {}

    # 4. Iterate downwards
    mapping = {}
    actual_row = row_groupe + 1
    col_color = col_groupe + 1

    while (
        actual_row < len(data_params)
        and data_params[actual_row][col_groupe].strip() != ""
    ):
        group_name = data_params[actual_row][col_groupe].strip()
        color = extract_rgb_from_cell_coords(
            metadata, actual_row, col_color, sheet_id=sheet_meta_idx
        )
        mapping[group_name] = color
        actual_row += 1

    mapping = {k: v for v, k in mapping.items()}  # type: ignore

    return mapping
