import re
import logging
from datetime import datetime
import dateparser
from babel.dates import format_date, format_time
import pandas as pd

# Configuration du logger spécifique
logger = logging.getLogger("cnum_parser")

def get_position_from_params(start, end, week, index_sheet, data):
    """Trouve les coordonnées de cellule pour un créneau horaire."""
    date_str = format_date(start, format="full", locale="fr_FR")
    if date_str not in index_sheet:
        logger.warning(f"Date non trouvée dans l'index : {date_str}")
        return None
    # On prend la première occurrence de la date
    date_pos = index_sheet[date_str][0]

    times_raw = [row[0] for row in data[date_pos[0] + 1 : date_pos[0] + 9]]
    t_start = [t.split("\n")[0].strip() for t in times_raw]
    t_end = [t.split("\n")[1].strip() for t in times_raw]

    map_start = {v: k + date_pos[0] for k, v in enumerate(t_start)}
    map_end = {v: k + date_pos[0] for k, v in enumerate(t_end)}

    h_start = start.strftime("%H:%M")
    h_end = end.strftime("%H:%M")

    if h_start not in map_start or h_end not in map_end:
        logger.warning(f"Heures non trouvées : {h_start}-{h_end}")
        return None

    r_start = map_start[h_start]
    r_end = map_end[h_end] + 1

    if not week:
        c_start, c_end = date_pos[1], date_pos[1] + 2
    elif week == "A":
        c_start, c_end = date_pos[1], date_pos[1] + 1
    else:
        c_start, c_end = date_pos[1] + 1, date_pos[1] + 2

    return [r_start + 1, r_end + 1, c_start, c_end]

def get_all_merges(sheet) -> list:
    try:
        spreadsheet = sheet.spreadsheet
        # On récupère les métadonnées spécifiquement pour cette feuille
        spreadsheet_data = spreadsheet.fetch_sheet_metadata({"fields": "sheets(properties,merges)"})
        for sheet_data in spreadsheet_data.get("sheets", []):
            if sheet_data.get("properties", {}).get("sheetId") == sheet.id:
                merges = sheet_data.get("merges", [])
                # S'assurer que le sheetId est bien présent dans chaque merge pour gspread
                for m in merges:
                    m["sheetId"] = sheet.id
                return merges
    except Exception as e:
        logger.error(f"Erreur get_all_merges : {e}")
    return []

def get_text_from_merged_cell(data, merge):
    try:
        return data[merge["startRowIndex"]][merge["startColumnIndex"]]
    except: return ""

def get_time_delta_from_merge(data, merge):
    """Logique robuste de récupération des dates et heures."""
    try:
        time_format = "%H:%M"
        start_row_id = merge["startRowIndex"]
        end_row_id = merge["endRowIndex"]
        start_col_id = merge["startColumnIndex"]
        
        row_dates = start_row_id
        found_date_line = False
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        
        while row_dates >= 0:
            line_content = " ".join(data[row_dates]).lower()
            if any(day in line_content for day in days_of_week):
                found_date_line = True
                break
            row_dates -= 1
            
        if not found_date_line: return (None, None)
            
        try:
            raw_start_str = data[start_row_id][0]
            raw_end_str = data[end_row_id - 1][0]
            time_start = [t.strip() for t in raw_start_str.split("\n")][0]
            time_end_parts = [t.strip() for t in raw_end_str.split("\n")]
            time_end = time_end_parts[1] if len(time_end_parts) > 1 else time_end_parts[0]
            
            time_start_obj = datetime.strptime(time_start, time_format).time()
            time_end_obj = datetime.strptime(time_end, time_format).time()
        except: return (None, None)
        
        target_cols = [start_col_id, start_col_id - 1]
        date_obj = None
        for col in target_cols:
            if col < 0: continue
            date_str = data[row_dates][col]
            parsed = dateparser.parse(date_str)
            if parsed:
                date_obj = parsed.date()
                break
        
        if not date_obj: return (None, None)
        return (datetime.combine(date_obj, time_start_obj), datetime.combine(date_obj, time_end_obj))
    except: return (None, None)

def parse_profs(text: str) -> list:
    bracket_match = re.search(r"\(([^a-z]+)\)", str(text))
    if bracket_match:
        return re.findall(r"[A-Z]{2,5}", bracket_match.group(1))
    return []

def clean_cours_name(cours: str):
    return str(cours).strip()

def extract_rgb_from_cell_coords(metadata, row, col, sheet_id: int = 1):
    try:
        sheet_data = None
        for s in metadata.get("sheets", []):
            if s.get("properties", {}).get("index") == sheet_id:
                sheet_data = s.get("data", [{}])[0]
                break
        if not sheet_data: sheet_data = metadata["sheets"][sheet_id]["data"][0]

        row_data = sheet_data.get("rowData", [])
        cell = row_data[row]["values"][col]
        rgb = cell.get("effectiveFormat", {}).get("backgroundColorStyle", {}).get("rgbColor", {})
        # On retourne un tuple simple de floats
        return (float(rgb.get("red", 0)), float(rgb.get("green", 0)), float(rgb.get("blue", 0)))
    except: return (1.0, 1.0, 1.0)

def extract_rgb_form_merge(metadata, merge, sheet_id: int = 1):
    return extract_rgb_from_cell_coords(metadata, merge["startRowIndex"], merge["startColumnIndex"], sheet_id)

def get_index_sheet(sheet):
    data = sheet.get_all_values()
    index_sheet = {}
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val not in index_sheet: index_sheet[val] = []
            index_sheet[val].append((r, c))
    return index_sheet

def get_merge_semaine(merge):
    try:
        s, e = merge["startColumnIndex"], merge["endColumnIndex"]
        if (e - s) == 2: return None
        if s in (1, 3, 6, 8, 11): return "A"
        if s in (2, 4, 7, 9, 12): return "B"
    except: pass
    return None

def parse_room(text: str) -> str:
    match = re.search(r"\[([^\]]+)\]", str(text))
    return "".join(re.findall(r"[A-Z0-9]+", match.group(1))) if match else None

def parse_type_cours(text: str) -> str:
    match = re.search(r"\"([^\"]+)\"", str(text))
    return "".join(re.findall(r"[A-Z]+", match.group(1))) if match else None

def get_dates_positions_from_data(data) -> list:
    pattern = r"^(\w+)\s+(\d{1,2})\s+(\w+)\s+(\d{4})$"
    positions = []
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            if re.match(pattern, str(cell)):
                positions.append([row_idx, col_idx])
    return positions
