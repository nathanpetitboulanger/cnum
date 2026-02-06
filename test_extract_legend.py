from datetime import datetime
from pickle import TRUE
from typing import Mapping
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.functions import extract_rgb_from_cell_coords
from gspread_formatting import *

from config import edt_sheet_id
from utils.functions import *


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
sheet = spreadsheet.get_worksheet(0)
data = sheet.get_all_values()

params = {
    "includeGridData": True,
    "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
}
meta_data = spreadsheet.fetch_sheet_metadata(params=params)


def extract_legend(
    meta_data: Mapping,
):
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


extract_name_from_code(data)
