import re
from gspread_dataframe import set_with_dataframe
import dateparser
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from utils.functions import *
from utils.dummies import *
from config import edt_sheet_id
import pandas as pd

"""
parse edt
"""


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
sheet = spreadsheet.get_worksheet(edt_sheet_id)
data = sheet.get_all_values()
all_merges = get_all_merges(sheet)

params = {
    "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))"
}
metadata = spreadsheet.fetch_sheet_metadata(params=params)

df = pd.DataFrame(columns=["cours", "start", "end", "prof", "RGB"])


for merge in all_merges:
    try:
        delta = get_time_delta_from_merge(data, merge)
        str_cours_raw = get_text_from_merged_cell(data, merge)
        prof = parse_profs(str_cours_raw)
        cours_str = clean_cours_name(str_cours_raw)
        color = extract_rgb_form_merge(metadata, merge)

        if str_cours_raw == "":
            raise ValueError("PAS DE COURS")

        row = [cours_str, delta[0], delta[1], prof, color]

        df.loc[len(df)] = row

    except Exception as e:
        print(e)
        pass


df["delta"] = df["end"] - df["start"]
df["delta"] = df["delta"].dt.total_seconds() / 3600


# Map names
corr_names = {
    "BP": "Benjamin Pey",
    "CF": "Clément Fabre",
    "DS": "David Sheeren",
    "JPS": "Jean",
    "LB": "Laurie Boithias",
    "LD": "Laurie Dunn",
    "RLH": "Lucas Hardouin",
    "MG": "Maritxu Guiresse",
    "ML": "Marc Lang",
    "RT": "Roman Teisserenc",
    "YG": "Youen Grusson",
    "SG": "Séraphine Grellier",
    "BD": "Bruno Dumora",
}
coor_names = pd.Series(corr_names)


def transformer_initiales(liste_initiales):
    if not isinstance(liste_initiales, list):
        return []
    return [coor_names.get(init, init) for init in liste_initiales]


df["prof"] = df["prof"].apply(transformer_initiales)


# Titre de la nouvelle feuille
new_sheet_title = "edt_clean"

try:
    new_sheet = spreadsheet.add_worksheet(
        title=new_sheet_title,
        rows="100",  # type: ignore
        cols="20",  # type: ignore
    )
except gspread.exceptions.APIError:
    new_sheet = spreadsheet.worksheet(new_sheet_title)

set_with_dataframe(new_sheet, df)


def calcul_and_display_prof_houres():
    def get_prof_total_hours(df, prof: str):
        df_filtered = df[df["prof"].apply(lambda x: any(prof in nom for nom in x))]
        return df_filtered["delta"].sum()

    prof_time_sum = {prof: get_prof_total_hours(df, prof) for prof in coor_names.values}

    df_bilan = pd.DataFrame(
        prof_time_sum.items(), columns=["Professeur", "Total Heures"]
    )
    data_to_upload = [df_bilan.columns.tolist()] + df_bilan.values.tolist()

    new_sheet.update(range_name="H1", values=data_to_upload)


calcul_and_display_prof_houres()
