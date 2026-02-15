import gspread
import pandas as pd
from src.utils.functions import extract_rgb_from_cell_coords

def get_mapping_dict_for_name(spreadsheet):
    """Extrait la correspondance Initiales -> Nom Complet depuis l'onglet Paramètres."""
    sheet = spreadsheet.worksheet("Paramètres")
    data = sheet.get_all_values()
    teacher_code = {}
    # Logique : colonne 3 code (ex: ML), colonne 4 nom (ex: Marc Lang)
    for row in data[1:]:
        if len(row) > 4 and row[4].strip():
            teacher_code[row[3]] = row[4]
    return teacher_code

def get_mapping_dict_for_group_color(spreadsheet):
    """Extrait la correspondance Couleur RGB -> Groupe (A, B, FI...) depuis l'onglet Paramètres."""
    sheet = spreadsheet.worksheet("Paramètres")
    data = sheet.get_all_values()
    
    # Trouver l'en-tête 'Groupes'
    row_g, col_g = -1, -1
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val == "Groupes":
                row_g, col_g = r, c
                break
    
    if row_g == -1: return {}
    
    params = {"includeGridData": True, "fields": "sheets(properties(title,sheetId,index),data(rowData(values(effectiveFormat(backgroundColorStyle)))))"}
    metadata = spreadsheet.fetch_sheet_metadata(params=params)
    
    # Trouver l'index réel de la feuille Paramètres
    sheet_index = 0
    for s in metadata["sheets"]:
        if s["properties"]["title"] == "Paramètres":
            sheet_index = s["properties"]["index"]
            break
            
    mapping = {}
    for r in range(row_g + 1, len(data)):
        if r >= len(data) or col_g + 1 >= len(data[r]): break
        group = data[r][col_g].strip()
        if not group: break
        color = extract_rgb_from_cell_coords(metadata, r, col_g + 1, sheet_id=sheet_index)
        mapping[str(color)] = group
    return mapping

def get_df_from_sheet_name(spreadsheet, sheet_name: str):
    """Charge un onglet spécifique sous forme de DataFrame."""
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_values()
    if not data: return pd.DataFrame()
    return pd.DataFrame(data[1:], columns=data[0])
