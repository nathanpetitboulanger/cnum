#%%
# Tests api google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from IPython.display import display


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
sheet = spreadsheet.sheet1  # Accède au premier onglet



# début du scraping 
data = sheet.get_all_values()
        #permet de récupérer toutes les valeurs sous forme de liste,

meta_data = spreadsheet.fetch_sheet_metadata()
print(meta_data)
        #Permet de récupérer les méta data sous la forme d'un gros dictionnaires
merges = meta_data["sheets"][0]["merges"]
        #Permet de récupérer la catégorie merges dans les méta data
merges_lundi = [merge for merge in merges if merge ["startColumnIndex"] == 1]
        #On demande de récupérer toutes les valeurs avec comme clé d'entrée en colonne 1


id_col_horaire = 0
        #Quand on fera des appels à la première colonne, on utilisera cet objet plutôpt que [0] par soucis de clarté

for merge in merges_lundi :
    #Pour chaque bloc présent dans merges_lundi
    start_row_id = merge["startRowIndex"]
    #On récupère dans le dictionnaire merge l'information de la ligne de début
    end_row_id = merge["endRowIndex"] - 1
    #Même chose mais pour la fin du bloc. On fait -1 car de base google envoie toutes les fins en +1
    col_id = merge["startColumnIndex"]
    #Permet d'obtenir le jour de la semaine
    content = data[start_row_id][col_id]
    #On va fouiller dans le tableau à la colonnes et à la ligne du bloc fusionné, pour obtenir le cours
    start_h = data[start_row_id][id_col_horaire]
    end_h = data[end_row_id][id_col_horaire]
    #Même chose, mais cette fois on reste dans la première colonne pour avoir les heures
    print(f"la phase {content} commence à {start_h}h et fini à {int(end_h) + 1}h")




############
# TEST pour récupérer les horaires des cours en jaune 

params = {'fields': 'sheets(data(rowData(values(userEnteredFormat/backgroundColor,effectiveValue))))'}
    #Permet de paramétrer le chemin d'accès exacte pour extraire les meta data, et ne pas se retrouver avec des miliers de lignes 
col_meta = spreadsheet.fetch_sheet_metadata(params)
    #Création d'un objet contenant les meta data de couleur 


rows = col_meta['sheets'][0]['data'][0]['rowData']
display(rows)
    #On créer un objet contenant les row data, on descend dans l'arborescence des dico












################### FONCTION

def get_text_from_any_cell(row, col, data, merges):
    """
    Récupère le texte d'une cellule, qu'elle soit fusionnée ou non.
    - row, col : coordonnées de la cellule ciblée
    - data : le tableau de valeurs (get_all_values)
    - merges : la liste des fusions (extraite des meta_data)
    """


















    

# %%
