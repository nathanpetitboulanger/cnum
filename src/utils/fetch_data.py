from oauth2client.service_account import ServiceAccountCredentials
from typing import Mapping
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


def get_df_from_sheet_index(sheet_index: int):
    """
    return the df of a clean_worksheet
    """

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
    sheet = spreadsheet.get_worksheet(3)
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0:1][0])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
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
    col_code = 0
    actual_row = 9
    col_teacher = 1
    teacher_code = {}

    while True:
        name = data[actual_row][col_teacher]

        if name is None or str(name).strip() == "":
            break

        name_cell = data[actual_row][col_code]
        teacher_code[name_cell] = name
        actual_row += 1

    return teacher_code
