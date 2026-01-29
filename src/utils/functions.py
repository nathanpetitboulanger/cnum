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
    spreadsheet,
    sheet_number: int = 1,
) -> list:
    """
    return all merged block in a sheet
    """

    metadata = spreadsheet.fetch_sheet_metadata()
    merges = metadata["sheets"][sheet_number]["merges"]
    return merges


################### FONCTION v2 ###########################
def get_text_from_merged_cell(data, merge):
    """
    Récupère le texte d'une cellule, qu'elle soit fusionnée ou non.
    """
    
        # 1. On identifie l'ancre (le coin haut-gauche)
        raw = merge["startRowIndex"]
        col = merge["startColumnIndex"]

    return data[raw][col]