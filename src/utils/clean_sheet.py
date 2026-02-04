def clear_all_values(spreadsheet, sheet_idx):
    """
    Génère une requête pour supprimer TOUTES les valeurs de la feuille
    tout en conservant le formatage (couleurs, bordures, etc.).
    """
    sheet = spreadsheet.get_worksheet(sheet_idx)
    request = {
        "repeatCell": {
            "range": {
                "sheetId": int(sheet.id),
                # En ne mettant pas de start/end Index,
                # Google applique la commande à toute la feuille.
            },
            "cell": {
                # On ne met rien dans 'userEnteredValue',
                # ce qui équivaut à "vide".
            },
            "fields": "userEnteredValue",
            # Crucial : On dit à Google de ne mettre à jour (vider)
            # QUE la valeur, sans toucher au format.
        }
    }
    spreadsheet.batch_update({"requests": [request]})


def reset_sheet_color(spreadsheet, sheet_idx):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    total_rows = sheet.row_count
    total_cols = sheet.col_count

    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": int(sheet.id),
                    "startRowIndex": 0,
                    "endRowIndex": total_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_cols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}
                    }
                },
                "fields": "userEnteredFormat.backgroundColor",
            }
        }
    ]

    try:
        spreadsheet.batch_update({"requests": requests})
        print(f"La feuille '{sheet.title}' est maintenant toute blanche.")
    except Exception as e:
        print(f"Erreur lors du blanchiment : {e}")


def unmerge_entire_sheet(spreadsheet, sheet_idx):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    total_rows = sheet.row_count
    total_cols = sheet.col_count

    requests = [
        {
            "unmergeCells": {
                "range": {
                    "sheetId": int(sheet.id),
                    "startRowIndex": 0,
                    "endRowIndex": total_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_cols,
                }
            }
        }
    ]
    try:
        spreadsheet.batch_update({"requests": requests})
    except Exception as e:
        print(f"Erreur : {e}")
