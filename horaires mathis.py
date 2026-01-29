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
sheet = spreadsheet.sheet1  # Accède au premier onglet

from collections import defaultdict

def edt_jour(worksheet, jour="Lundi"):
    """
    Crée un dictionnaire des matières pour un jour donné avec
    les heures de début et de fin.
    
    Parameters:
    - worksheet : gspread worksheet (feuille Google)
    - jour : str, nom de la colonne du jour ("Lundi", "Mardi", etc.)
    
    Returns:
    - dict : {matiere: [{"debut": "8h", "fin": "9h"}, ...]}
    """

    # 1️⃣ Lire toutes les données de la feuille
    data = worksheet.get_all_values()  
    # data est une liste de listes, chaque sous-liste = une ligne de la feuille

    # 2️⃣ Extraire les entêtes et les lignes de données
    headers = data[0]      # première ligne = noms des colonnes
    lignes = data[1:]      # reste = les données

    # 3️⃣ Trouver les indices des colonnes nécessaires
    idx_heure = headers.index("Heure")  # colonne des heures de début
    idx_jour = headers.index(jour)      # colonne du jour sélectionné

    # 4️⃣ Créer un dictionnaire vide pour stocker les résultats
    # Utilisation de defaultdict pour gérer plusieurs créneaux pour la même matière
    edt = defaultdict(list)

    # 5️⃣ Parcourir toutes les lignes sauf la dernière (pour prendre la prochaine heure)
    for i in range(len(lignes) - 1):
        ligne = lignes[i]            # ligne courante
        ligne_suivante = lignes[i+1] # ligne suivante pour l'heure de fin

        matiere = ligne[idx_jour].strip()  # retirer espaces autour
        heure_debut = ligne[idx_heure].strip()
        heure_fin = ligne_suivante[idx_heure].strip()

        # 6️⃣ Ignorer les cellules vides (pas de matière sur cette ligne)
        if not matiere:
            continue

        # 7️⃣ Ajouter le créneau au dictionnaire
        edt[matiere].append({
            "debut": f"{heure_debut}h",
            "fin": f"{heure_fin}h"
        })

    # 8️⃣ Convertir en dict normal (pas defaultdict)
    return dict(edt)
print(sheet.get_all_values())
