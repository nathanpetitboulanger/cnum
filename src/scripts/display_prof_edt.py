import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    edt_sheet_index,
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
from utils.fetch_data import get_df_from_sheet_index, get_df_from_sheet_name
from main_functions.build_sheets import create_preview_edt_prof

default_prof = "Marc Lang"


def main():
    parser = argparse.ArgumentParser(
        description="Display greyed out EDT for a professor.",
    )
    parser.add_argument(
        "--prof",
        type=str,
        required=True,
        help="Name of the professor",
        default=default_prof,
    )
    args = parser.parse_args()

    print(f"Connecting to Google Sheets for professor: {args.prof}")

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )

    client = gspread.authorize(creds)  # type: ignore
    spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)
    edt_sheet = spreadsheet.worksheet("EDT")

    df = get_df_from_sheet_name("edt_clean")

    sheet_prof = create_preview_edt_prof(
        spreadsheet,
        edt_sheet,
        df,
        args.prof,
    )

    print(f"Successfully created preview sheet: {sheet_prof.title}")


if __name__ == "__main__":
    main()
