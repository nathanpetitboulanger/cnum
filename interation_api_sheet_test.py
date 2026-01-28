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
    "nathan-petitboulanger-1b097cac714e.json",
    scope,  # type: ignore
)

client = gspread.authorize(creds)  # type: ignore


# 3. Ouverture du document
# Tu peux ouvrir par le titre exact ou par l'ID (présent dans l'URL)

sheet_name = "API"
spreadsheet = client.open(sheet_name)
sheet = spreadsheet.sheet1  # Accède au premier onglet


cell_list = sheet.range("A1:B100")
for cell in cell_list:
    cell.value = "Hello"
sheet.update_cells(cell_list)

cells = sheet.findall("Hello")
for cell in cells:
    cell.value = ""
sheet.update_cells(cells)
