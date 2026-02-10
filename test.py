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


def get_prof_hours_summary(df):
    """
    Prend le DF de l'EDT et retourne un résumé : Professeur | Total Heures
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Nettoyage rapide des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Séparation des professeurs (si plusieurs par ligne)
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 3. Calcul de la somme par professeur
    summary = df_exploded.groupby("prof")["delta"].sum().reset_index()
    summary.columns = ["professeur", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_total_hours_prof_by_week(df):
    """
    Retourne un DF du total d'heures par prof par semaine.
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Conversion en datetime et extraction de la semaine et du lundi
    df["start"] = pd.to_datetime(df["start"])
    df["week"] = df["start"].dt.strftime("%Y-W%V")
    df["date_lundi"] = df["start"].dt.to_period("W").dt.start_time

    # 2. Nettoyage des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 3. Séparation des professeurs
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 4. Calcul de la somme par semaine (et date) et par professeur
    summary = (
        df_exploded.groupby(["week", "date_lundi", "prof"])["delta"].sum().reset_index()
    )
    summary.columns = ["semaine", "date_lundi", "professeur", "total_hours"]

    return summary.sort_values(by=["semaine", "total_hours"], ascending=[True, False])


def get_spe_hours_summary(df):
    """
    Prend le DF de l'EDT et retourne un résumé : Cours | Total Heures
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Nettoyage rapide des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Séparation des professeurs (si plusieurs par ligne)
    df_exploded = (
        df.assign(prof=df["type_cours"].str.split(","))
        .explode("type_cours")
        .query("prof != ''")
    )

    df_exploded["type_cours"] = df_exploded["type_cours"].str.strip()

    # 3. Calcul de la somme par professeur
    summary = df_exploded.groupby("type_cours")["delta"].sum().reset_index()
    summary.columns = ["professeur", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


summary_df = get_prof_hours_summary(df)
print("--- Résumé Global ---")
print(summary_df)

summary_week_df = get_total_hours_prof_by_week(df)
print("\n--- Résumé par Semaine ---")
print(summary_week_df)
