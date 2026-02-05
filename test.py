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
from utils.fetch_data import get_df_from_sheet_index

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

df = get_df_from_sheet_index(3)

df["semaine"].unique()


index_sheet = get_index_sheet(sheet)
data = sheet.get_all_values()
##clean sheet
clean_all(spreadsheet, 4)
