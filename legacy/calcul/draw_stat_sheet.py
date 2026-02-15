import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import (
    format_cell_ranges,
    CellFormat,
    TextFormat,
    Color,
)
from concurrent.futures import ThreadPoolExecutor
from calcul.function_for_calculat_stats import (
    get_prof_hours_summary,
    get_total_hours_prof_by_week,
    get_type_cours_hours_summary,
    get_total_hours_type_cours_by_week,
    get_group_etudiant_hours_summary,
    get_total_hours_group_etudiant_by_week,
)
from utils.fetch_data import get_df_from_sheet_name, get_spreadsheet
from utils.clean_sheet import clean_all

# Table positions configuration
TABLE_CONFIG = {
    "prof": {
        "title": "Global Professor Summary",
        "col": 1,
    },
    "week": {"title": "Weekly Professor Summary", "col": 4},
    "type": {"title": "Global Type Summary", "col": 9},
    "week_type": {"title": "Weekly Type Summary", "col": 12},
    "group": {
        "title": "Global Group Summary",
        "col": 17,
    },
    "week_group": {
        "title": "Weekly Group Summary",
        "col": 20,
    },
}


def fetch_and_calculate_all_stats(df):
    """Calculates all statistical summaries."""
    print("Calculating statistics...")
    return {
        "prof": get_prof_hours_summary(df),
        "week": get_total_hours_prof_by_week(df),
        "type": get_type_cours_hours_summary(df),
        "week_type": get_total_hours_type_cours_by_week(df),
        "group": get_group_etudiant_hours_summary(df),
        "week_group": get_total_hours_group_etudiant_by_week(df),
    }


def prepare_stats_sheet(spreadsheet):
    """Retrieves or creates the 'stats' sheet and cleans it."""
    try:
        stats_sheet = spreadsheet.worksheet("stats")
    except gspread.exceptions.WorksheetNotFound:
        print("Creating 'stats' sheet...")
        stats_sheet = spreadsheet.add_worksheet(title="stats", rows="100", cols="30")

    print("Cleaning 'stats' sheet...")
    clean_all(spreadsheet, stats_sheet.index)
    return stats_sheet


def _write_single_table(stats_sheet, key, config, df):
    """Worker function to write a single table (Title + Data)."""
    # Title
    stats_sheet.update_acell(f"{chr(64 + config['col'])}1", config["title"])
    # Data
    set_with_dataframe(stats_sheet, df, row=2, col=config["col"])


def write_all_tables(stats_sheet, stats_dict):
    """Writes titles and DataFrames to the sheet in parallel."""
    print("Writing tables in parallel...")
    with ThreadPoolExecutor() as executor:
        # Launch all writes simultaneously
        futures = [
            executor.submit(
                _write_single_table, stats_sheet, key, config, stats_dict[key]
            )
            for key, config in TABLE_CONFIG.items()
        ]
        # Wait for all tasks to complete
        for future in futures:
            future.result()


def apply_modern_formatting(stats_sheet, stats_dict):
    """Applies formatting (Titles, Headers, Zebra)."""
    print("Applying formatting and zebra striping...")

    title_format = CellFormat(
        textFormat=TextFormat(
            bold=True, fontSize=12, foregroundColor=Color(0.2, 0.4, 0.6)
        ),
        horizontalAlignment="LEFT",
    )
    header_format = CellFormat(
        backgroundColor=Color(0.9, 0.9, 0.9),
        textFormat=TextFormat(bold=True),
        horizontalAlignment="CENTER",
    )
    zebra_format = CellFormat(backgroundColor=Color(0.95, 0.95, 1.0))

    format_ranges = []

    for key, config in TABLE_CONFIG.items():
        df = stats_dict[key]
        start_col = config["col"]
        end_col = start_col + len(df.columns) - 1
        end_col_letter = chr(64 + end_col)
        start_col_letter = chr(64 + start_col)

        # 1. Title Format (Row 1)
        format_ranges.append((f"{start_col_letter}1", title_format))

        # 2. Header Format (Row 2)
        format_ranges.append((f"{start_col_letter}2:{end_col_letter}2", header_format))

        # 3. Zebra Striping
        for i in range(len(df)):
            if i % 2 == 1:
                row_idx = 3 + i  # Row 3 is the first data row
                format_ranges.append(
                    (
                        f"{start_col_letter}{row_idx}:{end_col_letter}{row_idx}",
                        zebra_format,
                    )
                )

    format_cell_ranges(stats_sheet, format_ranges)


def draw_stats():
    """Main function orchestrating the stats update."""
    spreadsheet = get_spreadsheet()

    print("Fetching data from 'edt_clean'...")
    df = get_df_from_sheet_name("edt_clean")
    if df.empty:
        print("Error: DataFrame is empty.")
        return

    stats_dict = fetch_and_calculate_all_stats(df)
    stats_sheet = prepare_stats_sheet(spreadsheet)

    write_all_tables(stats_sheet, stats_dict)
    apply_modern_formatting(stats_sheet, stats_dict)

    print("Done! Statistics are available in the 'stats' sheet.")


if __name__ == "__main__":
    draw_stats()

