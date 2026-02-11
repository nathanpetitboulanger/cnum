import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
from scripts.backup_edt import main as backup_main
from scripts.generate_changes_visualisation import main as generate_viz


def main():
    # 0. Backup current EDT first for safety
    print("Pre-application backup...")
    backup_main()

    print("Connecting to Google Sheets...")
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )
    client = gspread.authorize(creds)  # type: ignore
    spreadsheet = client.open(DEFAULT_SPREADSHEET_NAME)

    try:
        drawing_sheet = spreadsheet.worksheet("drawing")
    except gspread.WorksheetNotFound:
        print("Error: 'drawing' sheet not found. Run draw_df.py first.")
        return

    try:
        edt_sheet = spreadsheet.worksheet("EDT")
    except gspread.WorksheetNotFound:
        print("Error: 'EDT' sheet not found.")
        return

    print(
        f"Applying 'drawing' (ID: {drawing_sheet.id}) to 'EDT' (ID: {edt_sheet.id})..."
    )

    # Use copyPaste request to copy everything from drawing to EDT
    # PASTE_NORMAL copies values, formulas, formats, and merges.
    body = {
        "requests": [
            {
                "copyPaste": {
                    "source": {
                        "sheetId": drawing_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": drawing_sheet.row_count,
                        "startColumnIndex": 0,
                        "endColumnIndex": drawing_sheet.col_count,
                    },
                    "destination": {
                        "sheetId": edt_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": drawing_sheet.row_count,
                        "startColumnIndex": 0,
                        "endColumnIndex": drawing_sheet.col_count,
                    },
                    "pasteType": "PASTE_NORMAL",
                    "pasteOrientation": "NORMAL",
                }
            }
        ]
    }

    spreadsheet.batch_update(body)
    print("Successfully overwritten 'EDT' with 'drawing' content and formatting.")

    # 4. Update visualisation and logs
    print("Updating history visualisation and logs...")
    generate_viz()


if __name__ == "__main__":
    main()
