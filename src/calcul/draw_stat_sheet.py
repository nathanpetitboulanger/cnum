import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import (
    format_cell_ranges,
    CellFormat,
    TextFormat,
    Color,
)
from calcul.function_for_calculat_stats import (
    get_prof_hours_summary,
    get_total_hours_prof_by_week,
    get_type_cours_hours_summary,
    get_group_etudiant_hours_summary,
)
from utils.fetch_data import get_df_from_sheet_name, get_spreadsheet
from utils.clean_sheet import clean_all

# Configuration des positions des tables
TABLE_CONFIG = {
    "prof": {
        "title": "Récapitulatif Global par Professeur",
        "col": 1,
        "col_letter": "B",
    },
    "week": {"title": "Récapitulatif Hebdomadaire", "col": 5, "col_letter": "H"},
    "type": {"title": "Récapitulatif par Type de Cours", "col": 11, "col_letter": "L"},
    "group": {
        "title": "Récapitulatif par Groupe Étudiant",
        "col": 15,
        "col_letter": "P",
    },
}


def fetch_and_calculate_all_stats(df):
    """Calcule tous les résumés statistiques."""
    print("Calcul des statistiques...")
    return {
        "prof": get_prof_hours_summary(df),
        "week": get_total_hours_prof_by_week(df),
        "type": get_type_cours_hours_summary(df),
        "group": get_group_etudiant_hours_summary(df),
    }


def prepare_stats_sheet(spreadsheet):
    """Récupère ou crée la feuille 'stats' et la nettoie."""
    try:
        stats_sheet = spreadsheet.worksheet("stats")
    except gspread.exceptions.WorksheetNotFound:
        print("Création de la feuille 'stats'...")
        stats_sheet = spreadsheet.add_worksheet(title="stats", rows="100", cols="30")

    print("Nettoyage de la feuille 'stats'...")
    clean_all(spreadsheet, stats_sheet.index)
    return stats_sheet


def write_all_tables(stats_sheet, stats_dict):
    """Écrit les titres et les DataFrames dans la feuille."""
    print("Écriture des tableaux...")
    for key, config in TABLE_CONFIG.items():
        df = stats_dict[key]
        # Titre
        stats_sheet.update_acell(f"{chr(64 + config['col'])}1", config["title"])
        # Données
        set_with_dataframe(stats_sheet, df, row=2, col=config["col"])


def apply_modern_formatting(stats_sheet, stats_dict):
    """Applique le formatage (Titres, Headers, Zebra)."""
    print("Application du formatage et zebra striping...")

    title_format = CellFormat(
        textFormat=TextFormat(
            bold=True, fontSize=12, foregroundColor=Color(0.2, 0.4, 0.6)
        ),
        horizontalAlignment="LEFT",
    )
    header_format = CellFormat(
        backgroundColor=Color(0.9, 0.9, 0.9),
        textFormat=TextFormat(bold=True),
        horizontalAlignment="CENTER",
    )
    zebra_format = CellFormat(backgroundColor=Color(0.95, 0.95, 1.0))

    format_ranges = []

    for key, config in TABLE_CONFIG.items():
        df = stats_dict[key]
        start_col = config["col"]
        end_col = start_col + len(df.columns) - 1
        end_col_letter = chr(64 + end_col)
        start_col_letter = chr(64 + start_col)

        # 1. Format Titre (Ligne 1)
        format_ranges.append((f"{start_col_letter}1", title_format))

        # 2. Format Header (Ligne 2)
        format_ranges.append((f"{start_col_letter}2:{end_col_letter}2", header_format))

        # 3. Zebra Striping
        for i in range(len(df)):
            if i % 2 == 1:
                row_idx = 3 + i  # Ligne 3 est la première ligne de données
                format_ranges.append(
                    (
                        f"{start_col_letter}{row_idx}:{end_col_letter}{row_idx}",
                        zebra_format,
                    )
                )

    format_cell_ranges(stats_sheet, format_ranges)


def draw_stats():
    """Fonction principale orchestrant la mise à jour des stats."""
    spreadsheet = get_spreadsheet()

    print("Récupération des données depuis 'edt_clean'...")
    df = get_df_from_sheet_name("edt_clean")
    if df.empty:
        print("Erreur : Le DataFrame est vide.")
        return

    stats_dict = fetch_and_calculate_all_stats(df)
    stats_sheet = prepare_stats_sheet(spreadsheet)

    write_all_tables(stats_sheet, stats_dict)
    apply_modern_formatting(stats_sheet, stats_dict)

    print("Terminé ! Les statistiques sont disponibles dans la feuille 'stats'.")


if __name__ == "__main__":
    draw_stats()

