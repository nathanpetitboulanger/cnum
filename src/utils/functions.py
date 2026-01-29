from gspread import spreadsheet
from datetime import datetime
import dateparser


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


def get_text_from_any_cell(row, col, data, merges):
    """
    Récupère le texte d'une cellule, qu'elle soit fusionnée ou non.
    """
    # Niveau 1 : Dans la fonction (4 espaces)
    # 1. On parcourt chaque zone fusionnée enregistrée par Google
    for merge in merges:
        # Niveau 2 : Dans la boucle FOR (8 espaces)
        # On vérifie si notre cellule est à l'intérieur de ce rectangle
        is_in_row_range = merge["startRowIndex"] <= row < merge["endRowIndex"]
        is_in_col_range = merge["startColumnIndex"] <= col < merge["endColumnIndex"]

        if is_in_row_range and is_in_col_range:
            # Niveau 3 : Dans la condition IF (12 espaces)
            # TROUVÉ ! C'est une cellule fusionnée.
            # On va chercher le texte à l'ANCRE (le début du merge)
            anchor_row = merge["startRowIndex"]
            anchor_col = merge["startColumnIndex"]
            return data[anchor_row][anchor_col]

    # Retour au Niveau 1 (4 espaces)
    # 2. Si on sort de la boucle sans rien avoir trouvé,
    # c'est que la cellule n'est pas fusionnée.
    # On renvoie simplement sa valeur brute.
    return data[row][col]


def get_all_merges(
    sheet,
) -> list:
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


def get_time_delta_from_merge(data, merge):
    id_col_time = 0
    time_format = "%H:%M"

    start_row_id = merge["startRowIndex"]
    end_row_id = merge["endRowIndex"]
    start_col_id = merge["startColumnIndex"]

    ## Récupération id dates

    row = start_row_id
    col = id_col_time

    actual_time_position = [row, col]
    actual_time = "date"
    while actual_time != "":
        actual_time_position[0] = actual_time_position[0] - 1
        row = actual_time_position[0]
        col = actual_time_position[1]
        actual_time = data[row][col]

    raw_start_str = data[start_row_id][id_col_time]
    raw_end_str = data[end_row_id][id_col_time]

    time_start = [time.strip() for time in raw_start_str.split("\n")][0]
    time_end = [time.strip() for time in raw_end_str.split("\n")][1]

    start_time_object = datetime.strptime(time_start, time_format).time()
    end_time_object = datetime.strptime(time_end, time_format).time()

    date_str = data[start_row_id - 1][start_col_id]

    date_obj = dateparser.parse(date_str).date()  # type: ignore

    start_datetime = datetime.combine(date_obj, start_time_object)
    end_datetime = datetime.combine(date_obj, end_time_object)

    return (start_datetime, end_datetime)
