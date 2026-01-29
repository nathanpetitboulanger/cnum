#Faire fonction qui récupère couleur d'un bloc et en argument col/ligne
#Utiliser la fonction de Nathan 

# Tests api google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Définir le périmètre (Scope)
# On définit ici que l'on veut accéder aux feuilles et au drive

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# 2. Authentification avec ton fichier JSON
# Remplace "nom_de_ta_cle.json" par le vrai nom de ton fichier
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "token.json",
    scope,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore


# 3. Ouverture du document
# Tu peux ouvrir par le titre exact ou par l'ID (présent dans l'URL)
sheet_name = "API"
spreadsheet = client.open(sheet_name)
sheet = spreadsheet.worksheet("EDT") # Accède à l'onglet EDT


def get_block_color(row, col):
    """Récupère la couleur d'un bloc dans la feuille Google Sheets.

    Args:
        row (int): Le numéro de la ligne (1-indexed).
        col (int): Le numéro de la colonne (1-indexed).

    Returns:
        dict: Un dictionnaire contenant les valeurs RGB de la couleur du bloc.
    """
    cell = sheet.cell(row, col)
    cell_format = sheet.get_format(cell.row, cell.col)
    bg_color = cell_format['backgroundColor']
    return bg_color




