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
from main_functions.build_sheets import (
    draw_sheet_from_df,
    draw_sheet_for_prof,
    create_preview_edt_prof,
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
from utils.fetch_data import get_df_from_sheet_index
from utils.detect_cell_positions import get_dates_positions_from_data


pio.renderers.default = "browser"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore
spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)

metadata = spreadsheet.fetch_sheet_metadata()

edt_sheet = spreadsheet.get_worksheet(edt_sheet_index)

# edt_copy = spreadsheet.duplicate_sheet(
#     edt_sheet.id, new_sheet_name="Copy EDT", insert_sheet_index=100
# )

data = edt_sheet.get_all_values()


dates_positions = get_dates_positions_from_data(data)


def get_request_reset_cells(sheet, row_id, col_id, nrows, ncols):
    pass


df = get_df_from_sheet_index(3)


df.prof.unique()

sheet_prof = create_preview_edt_prof(
    spreadsheet,
    edt_sheet,
    df,
    "Séraphine Grellier",
)


spreadsheet.del_worksheet(sheet_prof)
