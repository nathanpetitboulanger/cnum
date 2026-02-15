import os
import pandas as pd
from datetime import datetime
from config import (
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
from utils.fetch_data import get_df_from_sheet_name


def main():
    # 1. Configuration
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")

    # 2. Get current timestamp for filename and logging
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    log_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{log_time}] Starting backup of 'edt_clean'...")

    try:
        # 3. Fetch data from Google Sheets
        df = get_df_from_sheet_name("edt_clean")

        if df.empty:
            print(
                f"[{log_time}] Warning: The 'edt_clean' sheet appears to be empty. No backup created."
            )
            return

        # 4. Save to CSV in backups folder
        filename = f"edt_backup_{timestamp_str}.csv"
        file_path = os.path.join(backup_dir, filename)

        df.to_csv(file_path, index=False)

        # 5. Log success
        print(f"[{log_time}] Backup successfully saved to: {file_path}")
        print(f"[{log_time}] Backup record created for future rollback.")

    except Exception as e:
        print(f"[{log_time}] Error during backup: {e}")


if __name__ == "__main__":
    main()
