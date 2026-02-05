# tests api google sheet
import re
import dateparser
import ast
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import requests
from utils.buid_draw_requests import (
    get_all_requests_from_df,
    get_request_unmerge_entire_sheet,
    get_requests_reset_sheet_color,
    get_request_clear_all_values,
)
from utils.functions import get_best_coords_from_delta, get_index_sheet
import pandas as pd
import dateparser
from babel.dates import format_date, format_time
import numpy as np
from gspread.utils import rowcol_to_a1
from utils.fetch_data import get_df_from_sheet_index
from utils.clean_sheet import clean_all
from config import edt_sheet_index
from utils.functions import get_index_sheet

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


edt = spreadsheet.get_worksheet(edt_sheet_index)
data = edt.get_all_values()
index_sheet = get_index_sheet(edt)

df = get_df_from_sheet_index(sheet_index=3)
df = df.query("cours != ''")


draw_sheet = spreadsheet.get_worksheet(4)


requests_ = []

requests_.append(get_request_unmerge_entire_sheet(draw_sheet))
requests_.append(get_requests_reset_sheet_color(draw_sheet))
requests_.append(get_request_clear_all_values(draw_sheet))

requests_.extend(
    get_all_requests_from_df(
        df,
        index_sheet,
        draw_sheet.id,
        data,
    )
)


spreadsheet.batch_update({"requests": requests_})
