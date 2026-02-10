import subprocess
from utils.fetch_data import get_df_from_sheet_index
from main_functions.build_sheets import draw_sheet_for_prof
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    edt_sheet_index,
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)


subprocess.run(["uv", "run", "src/scripts/parse_edt.py"])

subprocess.run(["uv", "run", "src/scripts/draw_df.py"])

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore
spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
edt_sheet = spreadsheet.get_worksheet(edt_sheet_index)

df = get_df_from_sheet_index(3)
df.prof.unique()
PROF = "Marc Lang"


sheet_prof = draw_sheet_for_prof(
    df,
    spreadsheet,
    edt_sheet,
    PROF,
)

spreadsheet.del_worksheet(sheet_prof)
