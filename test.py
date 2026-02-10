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
from main_functions.build_sheets import (
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
)
from utils.detect_cell_positions import get_dates_positions_from_data


pio.renderers.default = "browser"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES,  # type: ignore
)
client = gspread.authorize(creds)  # type: ignore

spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
metadata = spreadsheet.fetch_sheet_metadata()


df = get_df_from_sheet_name()

stats_sheet = spreadsheet.worksheet("stats")


def calcul_and_display_prof_houres(df):
    """
    use df, the dataframe of edt_clean for display get_dates_positions_from_data
    """

    coors_names = get_mapping_dict_for_name(spreadsheet)

    def get_prof_total_hours(df, prof: str):
        df_filtered = df[df["prof"].apply(lambda x: any(prof in nom for nom in x))]
        return df_filtered["delta"].sum()

    prof_time_sum = {
        prof: get_prof_total_hours(
            df,
            prof,
        )
        for prof in coors_names.values
    }

    df_bilan = pd.DataFrame(
        prof_time_sum.items(), columns=["Professeur", "Total Heures"]
    )
    data_to_upload = [df_bilan.columns.tolist()] + df_bilan.values.tolist()

    stats_sheet.update(range_name="A1", values=data_to_upload)


calcul_and_display_prof_houres(df)
