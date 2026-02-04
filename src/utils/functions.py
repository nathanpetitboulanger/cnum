import re
from datetime import datetime

import dateparser
from babel.dates import format_date, format_time
from gspread import spreadsheet


def get_cell_color(spreadsheet, sheet_numbrer: int, row: int, col: int):
    """
    Retourne un tuple (R, G, B) entre 0 et 1 pour une cellule donnée.
    implémenté pour l'instant dans la sheet 1.
    """

    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    metadata = spreadsheet.fetch_sheet_metadata(params=params)

    try:
        cell = metadata["sheets"][sheet_numbrer]["data"][0]["rowData"][row]["values"][
            col
        ]
        color = (
            cell.get("effectiveFormat", {})
            .get("backgroundColorStyle", {})
            .get("rgbColor", {})
        )

        red = color.get("red", 0)
        green = color.get("green", 0)
        blue = color.get("blue", 0)

        return (red, green, blue)
    except (KeyError, IndexError):
        # Si la cellule n'existe pas ou n'a aucun format
        return (1, 1, 1)  # On retourne du blanc par défaut


def get_all_merges(
    sheet,
) -> list:  # type: ignore
    """
    return all merged block in a sheet
    """
    spreadsheet = sheet.spreadsheet
    spreadsheet_data = spreadsheet.fetch_sheet_metadata()

    for sheet_data in spreadsheet_data["sheets"]:
        if sheet_data.get("properties").get("sheetId") == sheet.id:
            return sheet_data.get("merges")


def get_text_from_merged_cell(data, merge):
    """
    return le text d'un merge.
    """
    raw = merge["startRowIndex"]
    col = merge["startColumnIndex"]
    return data[raw][col]


merge = {
    "sheetId": 739511890,
    "startRowIndex": 48,
    "endRowIndex": 50,
    "startColumnIndex": 9,
    "endColumnIndex": 10,
}


def get_time_delta_from_merge(data, merge):
    id_col_time = 0
    time_format = "%H:%M"

    start_row_id = merge["startRowIndex"]
    end_row_id = merge["endRowIndex"]
    start_col_id = merge["startColumnIndex"]

    ## Récupération id dates

    row_dates = start_row_id
    col = id_col_time
    actual_time_position = [row_dates, col]
    actual_time = "date"
    while actual_time != "":
        actual_time_position[0] = actual_time_position[0] - 1
        row_dates = actual_time_position[0]
        actual_time = data[row_dates][col]
        # print(f"acual_time : {actual_time}")
        # print(f"row_date : {row_dates}")

    raw_start_str = data[start_row_id][id_col_time]
    raw_end_str = data[end_row_id - 1][id_col_time]

    time_start = [time.strip() for time in raw_start_str.split("\n")][0]
    time_end = [time.strip() for time in raw_end_str.split("\n")][1]

    start_time_object = datetime.strptime(time_start, time_format).time()
    end_time_object = datetime.strptime(time_end, time_format).time()

    ##### GET DATE ON LEFT #####
    col_to_move_left = [2, 4, 7, 9, 12]
    if start_col_id in col_to_move_left:
        start_col_id -= 1

    date_str = data[row_dates][start_col_id]

    date_obj = dateparser.parse(date_str).date()  # type: ignore

    start_datetime = datetime.combine(date_obj, start_time_object)
    end_datetime = datetime.combine(date_obj, end_time_object)

    return (start_datetime, end_datetime)


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


def get_head_cell_coords_from_merge(merge):
    row_id = merge["startRowIndex"]
    col_id = merge["startColumnIndex"]
    return row_id, col_id


def extract_rgb_from_cell_coords(metadata, row, col, sheet_id: int = 1):
    sheet_data = metadata["sheets"][sheet_id]["data"][0]
    row_data = sheet_data.get("rowData", [])

    cell_values = row_data[row]["values"][col]
    rgb = cell_values["effectiveFormat"]["backgroundColorStyle"]["rgbColor"]
    return (rgb.get("red", 0), rgb.get("green", 0), rgb.get("blue", 0))


def extract_rgb_form_merge(metadata, merge, sheet_id: int = 1):
    row_id, col_id = get_head_cell_coords_from_merge(merge)
    return extract_rgb_from_cell_coords(metadata, row_id, col_id, sheet_id)


def extract_legend():
    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    meta_data = spreadsheet.fetch_sheet_metadata(params=params)

    col_nom = 13
    actual_row = 0
    col_color = 14
    color_mapping = {}

    while True:
        col = extract_rgb_from_cell_coords(meta_data, actual_row, col_color)

        if col == (1, 1, 1):
            break

        nom_cellule = data[actual_row][col_nom]
        color_mapping[nom_cellule] = col
        actual_row += 1

    return color_mapping


def get_index_sheet(sheet):
    """
    Return the index of the sheet once for the API rates actual_time_position
    """
    data = sheet.get_all_values()

    index_sheet = {}
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val not in index_sheet:
                index_sheet[val] = []
            index_sheet[val].append((r + 1, c + 1))
    return index_sheet


def get_best_coords_from_delta(start, end, index_sheet, data):
    """
    Return cours position form start and end. the index_sheet sheet is optainable with the function get_index_sheet
    Do not loop with get_index_sheet
    Same with data
    """

    start_date_str = format_date(start, format="full", locale="fr_FR")
    end_date_str = format_date(end, format="full", locale="fr_FR")

    start_hour_str = format_time(start, format="full", locale="fr_FR")
    end_hour_str = format_time(end, format="full", locale="fr_FR")

    index_date = index_sheet.get(end_date_str, [None])[0]

    index_col_date = index_date[1] - 1
    index_row_date = index_date[0]

    times_rows = data[index_row_date : index_row_date + 8]
    times_str = [[hour.strip() for hour in time[0].split("\n")] for time in times_rows]
    times = [
        [datetime.strptime(t, "%H:%M").time() for t in interval]
        for interval in times_str
    ]
    times = [
        [datetime.combine(start.date(), time) for time in interval]
        for interval in times
    ]

    best_idx_start_relative = min(
        range(len(times)), key=lambda i: abs(times[i][0] - start)
    )
    best_idx_end_relative = min(range(len(times)), key=lambda i: abs(times[i][0] - end))

    best_idx_start_relative = best_idx_start_relative + index_date[0]
    best_idx_end_relative = best_idx_end_relative + index_date[0]

    return (
        best_idx_start_relative + 1,
        best_idx_end_relative + 1,
        index_col_date,
        index_col_date + 2,
    )


def get_merge_semaine(merge):
    col_start = merge["startColumnIndex"]
    col_end = merge["endColumnIndex"]

    if (col_end - col_start) == 2:
        return None

    elif col_start in (1, 3, 6, 8, 11):
        return "A"

    elif col_start in (2, 4, 7, 9, 12):
        return "B"

    else:
        raise ValueError("Pas de merge trouvé")
