import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
from utils.fetch_data import get_df_from_sheet_name
from main_functions.build_sheets import create_preview_edt_full


def main():
    print("Connecting to Google Sheets for full EDT drawing")

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )

    client = gspread.authorize(creds)  # type: ignore
    spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
    edt_sheet = spreadsheet.worksheet("EDT")

    print("Fetching data from 'edt_clean'...")
    df = get_df_from_sheet_name("edt_clean")
    df = df.query("cours != ''")

    print("Creating full preview with skeleton on 'drawing' sheet...")
    sheet_draw = create_preview_edt_full(
        spreadsheet,
        edt_sheet,
        df,
    )

    print(f"Successfully created/updated drawing sheet: {sheet_draw.title}")


if __name__ == "__main__":
    main()
