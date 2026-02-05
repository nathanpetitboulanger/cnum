# tests api google sheet
import re
import dateparser
import ast
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from pandas.core.tools.datetimes import should_cache
import requests
from main_functions.build_sheets import draw_sheet_from_df, draw_sheet_for_prof
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
from config import edt_sheet_index
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
draw_sheet = spreadsheet.get_worksheet(4)
edt_sheet = spreadsheet.get_worksheet(edt_sheet_index)


df = get_df_from_sheet_index(3)
PROF = "Séraphine Grellier"

sheet_prof = draw_sheet_for_prof(
    df,
    spreadsheet,
    edt_sheet,
    PROF,
)

spreadsheet.del_worksheet(sheet_prof)
