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

#%%
def get_block_color(block):
    """
    Récupère la couleur de fond d'un bloc de cellules (ou d'une cellule fusionnée).
    Prend en argument un dictionnaire 'block' contenant les index (0-indexed).
    """

    # 1. On construit l'adresse de la zone. On prend le nom de l'onglet (sheet.title),
    # on ajoute R et C devant les chiffres pour parler le langage "R1C1" de Google. 
    # On fait +1 sur les points de départ car Sheets commence à 1 et ton code à 0
    range_a1 = (
        f"'{sheet.title}'!" #Identification de l'onglet. ! est le séparateur standard entre le nom de la feuille et la feuille
        f"R{block['startRowIndex'] + 1}C{block['startColumnIndex'] + 1}:"#
        f"R{block['endRowIndex']}C{block['endColumnIndex']}"
    )

    # 2. PRÉPARATION DES PARAMÈTRES POUR L'API
    # On crée un dictionnaire de paramètres. includeGridData: True dit à Google : "Ne me donne pas juste le titre du fichier, 
    # donne-moi le contenu détaillé (couleurs, texte) des cellules dans la zone range_a1
    params = {
        "includeGridData": True,
        "ranges": [range_a1] 
    }

    try:
        # 3. RÉCUPÉRATION DES MÉTADONNÉES
        metadata = spreadsheet.fetch_sheet_metadata(params=params)
        
        # 4. ACCÈS À LA CELLULE (Haut à gauche du bloc)
        cell_data = metadata["sheets"][0]["data"][0]["rowData"][0]["values"][0]
        
        # 5. EXTRACTION DU FORMAT UTILISATEUR
        fmt = cell_data.get("userEnteredFormat", {})
        
        # On vérifie les deux types de stockage de couleur de Google
        color_style = fmt.get("backgroundColorStyle", {})
        color_dict = color_style.get("rgbColor") or fmt.get("backgroundColor")

        # 6. CONVERSION EN TUPLE (R, V, B)
        # Si color_dict est vide (aucune couleur), on retourne du blanc (1.0, 1.0, 1.0)
        if not color_dict:
            return (1.0, 1.0, 1.0)
            
        # On utilise .get(..., 0.0) car Google n'envoie pas la clé si la valeur est 0
        r = color_dict.get('red', 0.0)
        g = color_dict.get('green', 0.0)
        b = color_dict.get('blue', 0.0)
        
        return (r, g, b)

    except Exception as e:
        # En cas d'erreur (ex: mauvaise plage), on renvoie du blanc par défaut
        print(f"Erreur lors de la récupération : {e}")
        return (1.0, 1.0, 1.0)

#%%
# Test block B7
dummie_block_B7 = {
    "startRowIndex": 6,
    "endRowIndex": 7,
    "startColumnIndex": 1,
    "endColumnIndex": 2,
}

color = get_block_color(dummie_block_B7)
print(f"Couleur du bloc : {color}")
#%%Test Block I11
dummie_block_I11 = {
    "startRowIndex": 10,
    "endRowIndex": 11,
    "startColumnIndex": 8,
    "endColumnIndex": 9
}

# Test avec ton dummie_block
color = get_block_color(dummie_block_I11)
print(f"Résultat : {color}")


# %%
