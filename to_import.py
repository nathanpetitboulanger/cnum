# to import in functions.py

from gspread_formatting import *


def extract_legend():
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
    sheet = spreadsheet.get_worksheet(6)
    data = sheet.get_all_values()

    params = {
        "includeGridData": True,
        "fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))",
    }
    meta_data = spreadsheet.fetch_sheet_metadata(params=params)

    col_nom = 13
    actual_row = 0
    col_color = 14
    color_mapping = {}

    while True:
        col = extract_rgb_from_cell_coords(meta_data, actual_row, col_color)

        if col == (1, 1, 1):
            break

        nom_cellule = data[actual_row][col_nom]
        color_mapping[nom_cellule] = col
        actual_row += 1

    color_mapping_reversed = {couleur: nom for nom, couleur in color_mapping.items()}

    return color_mapping_reversed


def add_col_group_to_df_with_RGB(df):
    cours_legend = extract_legend()
    cours_legend_pd = pd.Series(cours_legend)
    df["type_cours"] = df["RGB"].map(cours_legend_pd)
    return df


def calcul_and_display_group_hours():
    sum_hours_by_class = df.groupby("type_cours")["delta"].sum().reset_index()
    data_to_send = [
        sum_hours_by_class.columns.tolist()
    ] + sum_hours_by_class.values.tolist()

    new_sheet.update(range_name="P1", values=data_to_send)

    header_format = CellFormat(
        backgroundColor=color(0.2, 0.2, 0.2),  # Gris foncé
        textFormat=textFormat(
            bold=True, foregroundColor=color(1, 1, 1)
        ),  # Blanc et Gras
        horizontalAlignment="CENTER",
    )

    body_format = CellFormat(
        horizontalAlignment="RIGHT",
        numberFormat=numberFormat(
            type="NUMBER", pattern='0.00 "h"'
        ),  # Ajoute "h" automatiquement
    )

    format_cell_range(new_sheet, "P1:Q1", header_format)

    last_row = len(data_to_send)
    format_cell_range(new_sheet, f"P2:Q{last_row}", body_format)
