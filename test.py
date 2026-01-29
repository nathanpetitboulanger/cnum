# Tests api google sheet
import re
import dateparser
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.functions import *
from src.utils.dummies import *

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

sheet = spreadsheet.get_worksheet(1)
data = sheet.get_all_values()
all_merges = get_all_merges(sheet)
merge = all_merges[3]

data


delta = get_time_delta_from_merge(data, merge)


df = pd.DataFrame(columns=["cours", "start", "end", "prof"])

for merge in all_merges:
    try:
        delta = get_time_delta_from_merge(data, merge)
        str_cours_raw = get_text_from_merged_cell(data, merge)
        prof = parse_profs(str_cours_raw)
        cours_str = clean_cours_name(str_cours_raw)

        if str_cours_raw == "":
            raise ValueError("PAS DE COURS")

        row = [cours_str, delta[0], delta[1], prof]

        df.loc[len(df)] = row

    except Exception as e:
        print(e)
        pass


df["delta"] = df["end"] - df["start"]
df["delta"] = df["delta"].dt.total_seconds() / 3600


df.to_csv("final.csv")
