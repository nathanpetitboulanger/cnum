# tests api google sheet
import re
import dateparser
import ast
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import requests
from utils.draw_function import (
    merge_cells_batch,
    color_cells_batch,
    write_cells_batch,
    get_position_from_params,
)
from utils.clean_sheet import clean_all
from utils.functions import get_best_coords_from_delta, get_index_sheet
import pandas as pd
import dateparser
from babel.dates import format_date, format_time
import numpy as np
from utils.buid_draw_requests import (
    get_merge_request,
    get_color_request,
    get_write_request,
    get_all_requests_from_df,
)
from gspread.utils import rowcol_to_a1
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

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
sheet_id = sheet.id

sheet = spreadsheet.get_worksheet(1)

data = sheet.get_all_values()


index_sheet = get_index_sheet(sheet)
data = sheet.get_all_values()


##clean sheet
clean_all(spreadsheet, 4)

all_requests = get_all_requests_from_df(
    df,
    index_sheet,
    sheet_id,
    data,
)

spreadsheet.batch_update({"requests": [all_requests]})

d_sheet = spreadsheet.get_worksheet(4)


def merge_cells(sheet, start_row, end_row, start_col, end_col):
    start = rowcol_to_a1(start_row, start_col)
    end = rowcol_to_a1(end_row, end_col)
    plage = f"{start}:{end}"
    sheet.merge_cells(plage)


def color_cell(sheet, row, col, rgb):
    position = rowcol_to_a1(row, col)
    sheet.format(
        position, {"backgroundcolor": {"red": rgb[0], "green": rgb[1], "blue": rgb[2]}}
    )


merge_cells(d_sheet, 1, 2, 4, 5)
color_cell(d_sheet, 1, 4, (1, 0, 0))


unmerge_entire_sheet(spreadsheet, sheet_idx=4)
reset_sheet_color(spreadsheet, sheet_idx=4)


d_sheet.format("A1", {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}})
d_sheet.format("A1", {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}})
