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

merge = {
    "sheetId": 739511890,
    "startRowIndex": 6,
    "endRowIndex": 10,
    "startColumnIndex": 3,
}

merge = {
    "sheetId": 739511890,
    "startRowIndex": 70,
    "endRowIndex": 72,
    "startColumnIndex": 11,
    "endColumnIndex": 12,
}


delta = get_time_delta_from_merge(data, merge)


def parse_profs(text: str) -> list[str] | None:
    bracket_match = re.search(r"\(([^a-z]+)\)", text)
    if bracket_match:
        content = bracket_match.group(1)
        initiales = re.findall(r"[A-Z]{2}", content)
        return initiales
    else:
        return


def clean_cours_name(cours: str):
    pattern = r"\s*\([A-Z\s-]+\)"
    cleaned_text = re.sub(pattern, "", cours).strip()
    return cleaned_text


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
