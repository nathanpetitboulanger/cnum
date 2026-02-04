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
from utils.clean_sheet import reset_sheet_color, clear_all_values, unmerge_entire_sheet
from utils.functions import get_best_coords_from_delta, get_index_sheet
import pandas as pd
import dateparser
from babel.dates import format_date, format_time
import numpy as np
from utils.buid_draw_requests import (
    get_merge_request,
    get_color_request,
    get_write_request,
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

df = (
    (pd.read_csv("finale.csv").drop("Unnamed: 0", axis=1).sort_values("start"))
    .reset_index(drop=True)
    .reset_index()
)

# df = df.query("semaine == 'B'")

# px.scatter(df, ["start", "end"], "index")


df["start"] = pd.to_datetime(df["start"])

df["end"] = pd.to_datetime(df["end"])
df = df.sort_values("delta", ascending=False)

row_test = 1

index_sheet = get_index_sheet(sheet)
data = sheet.get_all_values()

##clean sheet
unmerge_entire_sheet(spreadsheet, sheet_idx=4)
reset_sheet_color(spreadsheet, sheet_idx=4)
clear_all_values(spreadsheet, sheet_idx=4)

all_requests = []

for k in range(len(df)):
    row_test = k
    start = df.iloc[row_test]["start"]
    end = df.iloc[row_test]["end"]
    week = df.iloc[row_test]["semaine"]
    value = df.iloc[row_test]["cours"]
    rgb_str = df.iloc[row_test]["RGB"]
    rgb = ast.literal_eval(rgb_str)

    positions = get_position_from_params(
        start,
        end,
        week,
        index_sheet,
        data,
    )

    all_requests.append(get_merge_request(sheet_id, *positions))
    all_requests.append(
        get_color_request(sheet_id, positions[0], col=positions[2], rgb=rgb)
    )
    all_requests.append(
        get_write_request(sheet_id, positions[0], positions[2], value=value)
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
