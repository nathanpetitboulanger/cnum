import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from config import edt_sheet_index, CREDENTIALS_FILE, SCOPES, DEFAULT_SPREADSHEET_NAME
from utils.dummies import *
from utils.functions import *
from utils.fetch_data import extract_name_from_code

"""
parse edt
"""

print("Start parsing EDT")

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore
spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
sheet = spreadsheet.get_worksheet(edt_sheet_index)
data = sheet.get_all_values()
all_merges = get_all_merges(sheet)

params = {
    "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))"
}
metadata = spreadsheet.fetch_sheet_metadata(params=params)  # type: ignore

df = pd.DataFrame(
    columns=["cours", "start", "end", "prof", "RGB", "semaine", "salle", "type_cours"]
)

str_cours_raw

for merge in all_merges:
    try:
        delta = get_time_delta_from_merge(data, merge)
        str_cours_raw = get_text_from_merged_cell(data, merge)
        prof = parse_profs(str_cours_raw)
        cours_str = clean_cours_name(str_cours_raw)
        color = extract_rgb_form_merge(metadata, merge)
        semaine = get_merge_semaine(merge)
        salle = parse_room(str_cours_raw)
        type_cours = parse_type_cours(str_cours_raw)

        if str_cours_raw == "":
            raise ValueError("PAS DE COURS")

        row = [cours_str, delta[0], delta[1], prof, color, semaine, salle, type_cours]

        df.loc[len(df)] = row

    except Exception as e:
        pass

df["end"] = pd.to_datetime(df["end"])
df["start"] = pd.to_datetime(df["start"])

df["delta"] = df["end"] - df["start"]
df["delta"] = df["delta"].dt.total_seconds() / 3600


def get_mapping_dict_for_name(spreadsheet):
    sheet = spreadsheet.worksheet("Paramètres")  # type: ignore
    data_params = sheet.get_all_values()
    names_codes = extract_name_from_code(data_params)

    coodes_names = pd.Series(names_codes)
    return coodes_names


corr_names = get_mapping_dict_for_name(spreadsheet)


def transformer_initiales(liste_initiales):
    """
    Convertit une liste d'initiales de professeurs (ex: ['ML', 'BP'])
    en leurs noms complets respectifs en utilisant le dictionnaire de correspondance.
    """
    if not isinstance(liste_initiales, list):
        return []
    return [corr_names.get(init, init) for init in liste_initiales]


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


df_export = df.copy()
df_export["prof"] = df_export["prof"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else str(x)
)


set_with_dataframe(new_sheet, df_export)

df.to_csv("finale.csv")


print("Parsing finish")
