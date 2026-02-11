import re
import gspread
from gspread_formatting import *
import pandas as pd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import concurrent.futures
from config import (
    edt_sheet_index,
    CREDENTIALS_FILE,
    SCOPES,
    DEFAULT_SPREADSHEET_NAME,
)
from utils import fetch_data
from utils.functions import *
from utils.fetch_data import (
    extract_name_from_code,
    get_mapping_dict_for_group_color,
    get_mapping_dict_for_name,
)

pd.set_option("display.max_rows", 500)


def connect_to_gsheets():
    """Handles authentication and returns the spreadsheet object."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        SCOPES,  # type: ignore
    )
    client = gspread.authorize(creds)  # type: ignore
    return client.open(DEFAULT_SPREADSHEET_NAME)


def fetch_raw_data(spreadsheet):
    """Fetches raw data, merges, and metadata from the EDT sheet."""
    sheet = spreadsheet.worksheet("EDT")
    data = sheet.get_all_values()
    all_merges = get_all_merges(sheet)

    params = {
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))"
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)  # type: ignore
    return data, all_merges, metadata


def parse_merges_to_df(data, all_merges, metadata):
    """Iterates over merges to extract course information into a DataFrame."""
    rows = []
    for merge in all_merges:
        try:
            delta_times = get_time_delta_from_merge(data, merge)
            str_cours_raw = get_text_from_merged_cell(data, merge)

            if str_cours_raw == "":
                continue

            date_pattern = r"\d{4}"
            print(str_cours_raw)
            if re.search(date_pattern, str_cours_raw):
                print(f"Date {str_cours_raw} out")
                raise ValueError("Date")

            prof_initials = parse_profs(str_cours_raw)
            cours_str = clean_cours_name(str_cours_raw)
            color = extract_rgb_form_merge(metadata, merge)
            semaine = get_merge_semaine(merge)
            salle = parse_room(str_cours_raw)
            type_cours = parse_type_cours(str_cours_raw)

            rows.append(
                [
                    cours_str,
                    delta_times[0],
                    delta_times[1],
                    prof_initials,
                    color,
                    semaine,
                    salle,
                    type_cours,
                ]
            )
        except Exception as e:
            print(e)
            pass

    df = pd.DataFrame(
        rows,
        columns=[
            "cours",
            "start",
            "end",
            "prof",
            "RGB",
            "semaine",
            "salle",
            "type_cours",
        ],  # type: ignore
    )
    return df


# spredsheet = connect_to_gsheets()
#
# data, all_merges, metadata = fetch_raw_data(spredsheet)
#
# df = parse_merges_to_df(data, all_merges, metadata)
#
# df.prof


def process_dataframe(df, spreadsheet):
    """Cleans data, calculates durations, and maps names/groups."""
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])

    # Duration in hours
    df["delta"] = (df["end"] - df["start"]).dt.total_seconds() / 3600

    # Group mapping
    color_mapping = get_mapping_dict_for_group_color(spreadsheet)
    df["groupe_etudiant"] = df["RGB"].map(color_mapping)  # type: ignore

    # Teacher names normalization
    corr_names = get_mapping_dict_for_name(spreadsheet)

    def transformer_initiales(liste_initiales):
        if not isinstance(liste_initiales, list):
            return []
        return [corr_names.get(init, init) for init in liste_initiales]

    df["prof"] = df["prof"].apply(transformer_initiales)
    return df


def _export_edt_clean(df, spreadsheet):
    """Internal function to export raw data to 'edt_clean'."""
    clean_sheet_title = "edt_clean"
    try:
        clean_sheet = spreadsheet.add_worksheet(
            title=clean_sheet_title, rows=100, cols=20
        )
    except gspread.exceptions.APIError:
        clean_sheet = spreadsheet.worksheet(clean_sheet_title)

    df_export = df.copy()
    df_export["prof"] = df_export["prof"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else str(x)
    )
    set_with_dataframe(clean_sheet, df_export)
    print(" - 'edt_clean' updated.")


def _export_readable_edt(df, spreadsheet):
    """Internal function to export human-readable data to 'Données Propres'."""
    readable_title = "Données Propres"
    try:
        readable_sheet = spreadsheet.add_worksheet(
            title=readable_title, rows=100, cols=20
        )
    except gspread.exceptions.APIError:
        readable_sheet = spreadsheet.worksheet(readable_title)

    df_readable = df.copy()
    df_readable["prof"] = df_readable["prof"].apply(lambda x: ", ".join(x))
    df_readable["jour"] = df_readable["start"].dt.strftime("%A %d %B")
    df_readable["heure_debut"] = df_readable["start"].dt.strftime("%H:%M")
    df_readable["heure_fin"] = df_readable["end"].dt.strftime("%H:%M")

    df_final = df_readable[["jour", "heure_debut", "heure_fin", "cours", "prof"]]

    readable_sheet.clear()
    set_with_dataframe(readable_sheet, df_final)

    # Formatting readable sheet
    fmt = cellFormat(  # type: ignore
        backgroundColor=color(0.9, 0.9, 0.9),  # type: ignore
        textFormat=textFormat(bold=True),  # type: ignore
        horizontalAlignment="CENTER",
    )
    format_cell_range(readable_sheet, "A1:E1", fmt)
    set_frozen(readable_sheet, rows=1)
    print(" - 'Données Propres' updated.")


def export_to_google_sheets(df, spreadsheet):
    """Creates/Updates sheets in parallel using multithreading."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_export_edt_clean, df, spreadsheet),
            executor.submit(_export_readable_edt, df, spreadsheet),
        ]
        concurrent.futures.wait(futures)


def main():
    print("Start parsing EDT...")
    spreadsheet = connect_to_gsheets()

    data, all_merges, metadata = fetch_raw_data(spreadsheet)
    df = parse_merges_to_df(data, all_merges, metadata)
    df = process_dataframe(df, spreadsheet)

    print(f"Parsed {len(df)} courses. Exporting...")
    export_to_google_sheets(df, spreadsheet)
    df.to_csv("finale.csv", index=False)

    print("Parsing finished successfully.")


if __name__ == "__main__":
    main()

    df = pd.read_csv("finale.csv")
    df.query("prof.str.contains('Marc')")
