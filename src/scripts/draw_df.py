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
    unmerge_entire_sheet,
    reset_sheet_color,
    write_cells_batch,
)
from utils.functions import get_best_coords_from_delta, get_index_sheet
import pandas as pd
import dateparser
from babel.dates import format_date, format_time
import numpy as np
from gspread.utils import rowcol_to_a1
# import plotly.express as px
# import plotly.io as

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

df = pd.read_csv("finale.csv").drop("Unnamed: 0", axis=1)


df["start"] = pd.to_datetime(df["start"])

df["end"] = pd.to_datetime(df["end"])
df = df.sort_values("delta", ascending=False)

start = df.iloc[0]["start"]
end = df.iloc[0]["end"]

index_sheet = get_index_sheet(sheet)
data = sheet.get_all_values()

unmerge_entire_sheet(spreadsheet, sheet_idx=4)
reset_sheet_color(spreadsheet, sheet_idx=4)


for _, cell in df.head(15).iterrows():
    start = cell.start
    end = cell.end
    week = cell.semaine
    value = cell.cours
    cell_data = list(get_best_coords_from_delta(start, end, index_sheet, data))
    start_row_index = cell_data[0]
    end_col_index = cell_data[1]
    start_col_index = cell_data[2]
    print(cell)
    print(cell_data)
    print(start, end)
    merge_cells_batch(spreadsheet, [cell_data + [week]], sheet_idx=4)
    color_cells_batch(
        spreadsheet,
        cell_data=[[start_row_index, start_col_index, ast.literal_eval(cell.RGB)]],
        sheet_idx=4,
    )
    write_cells_batch(
        spreadsheet,
        cell_data=[[start_row_index, start_col_index, value]],
        sheet_idx=4,
    )
