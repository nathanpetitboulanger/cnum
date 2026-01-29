# Tests api google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "token.json",
    scope,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore


sheet_name = "API"
spreadsheet = client.open(sheet_name)
sheet = spreadsheet.sheet1  # Accède au premier onglet

# donne l'emploie du temps de 1j

data = sheet.get_all_values()
meta_data = spreadsheet.fetch_sheet_metadata()
merges = meta_data["sheets"][0]["merges"]
merges_lundi = [merge for merge in merges if merge["startColumnIndex"] == 1]
id_col_horaire = 0
for merge in merges_lundi:
    start_row_id = merge["startRowIndex"]
    end_row_id = merge["endRowIndex"] - 1
    col_id = merge["startColumnIndex"]
    content = data[start_row_id][col_id]
    start_h = data[start_row_id][id_col_horaire]
    end_h = data[end_row_id][id_col_horaire]
    print(f" la phase {content} commence à {start_h}h et fini à {int(end_h) + 1}h")

# detection des couleurs
params = {
    "includeGridData": True,
    "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
}

metadata = spreadsheet.fetch_sheet_metadata(params=params)

row = 2
col = 1


def get_cell_color(spreadsheet, sheet_numbrer: int, row: int, col: int):
    """
    Retourne un tuple (R, G, B) entre 0 et 1 pour une cellule donnée.
    implémenté pour l'instant dans la sheet 1.
    """
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


# Utilisation :
couleur = get_cell_color(metadata, sheet_numbrer=0, row=3, col=2)
print(f"La couleur est : {couleur}")
