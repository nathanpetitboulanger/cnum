# tests api google sheet
from os import stat
import re
import dateparser
import ast
import gspread
from datetime import datetime
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from pandas.core.tools.datetimes import should_cache
import requests
from global_draw_functions.build_sheets import (
    draw_sheet_from_df,
)
from utils import fetch_data
from utils.clean_sheet import clean_all
from utils.functions import get_best_coords_from_delta, get_index_sheet
import pandas as pd
import dateparser
from babel.dates import format_date, format_time
import numpy as np
from utils.buid_draw_requests import (
    get_merge_request,
    get_color_request,
    get_request_clear_all_values,
    get_write_request,
    get_all_requests_from_df,
)
from gspread.utils import rowcol_to_a1
import plotly.express as px
from config import (
    edt_sheet_index,
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
import plotly.io as pio
from utils.fetch_data import (
    get_df_from_sheet_index,
    get_df_from_sheet_name,
    get_mapping_dict_for_name,
    get_mapping_dict_for_group_color,
    extract_legend,
)
from utils.detect_cell_positions import get_dates_positions_from_data
from calcul.function_for_calculat_stats import (
    get_prof_hours_summary,
    get_total_hours_prof_by_week,
    get_type_cours_hours_summary,
)

pio.renderers.default = "browser"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES,  # type: ignore
)
client = gspread.authorize(creds)  # type: ignore

spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
meta_data = spreadsheet.fetch_sheet_metadata()
data = spreadsheet.worksheet("Paramètres").get_all_values()


df = get_df_from_sheet_name("edt_clean")
stats_sheet = spreadsheet.worksheet("")


summary_df = get_prof_hours_summary(df)
print("--- Résumé Global ---")
print(summary_df)

summary_week_df = get_total_hours_prof_by_week(df)
print("\n--- Résumé par Semaine ---")
print(summary_week_df)
