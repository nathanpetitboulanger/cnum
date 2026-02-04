print("RELOAD")
import numpy as np
import pandas as pd
from babel.dates import format_date, format_time


def merge_cells_batch(spreadsheet, cells_data, sheet_idx):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    for (
        start_row_index,
        end_row_index,
        start_col_idx,
        end_col_idx,
        week,
    ) in cells_data:
        if pd.isna(week):
            requests.append(
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": start_row_index - 1,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": start_col_idx,
                            "endColumnIndex": end_col_idx,
                        },
                        "mergeType": "MERGE_ALL",
                    }
                }
            )
        elif week == "A":
            requests.append(
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": start_row_index - 1,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": start_col_idx,
                            "endColumnIndex": end_col_idx - 1,
                        },
                        "mergeType": "MERGE_ALL",
                    }
                }
            )
        elif week == "B":
            requests.append(
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": start_row_index - 1,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": start_col_idx + 1,
                            "endColumnIndex": end_col_idx,
                        },
                        "mergeType": "MERGE_ALL",
                    }
                }
            )
        else:
            raise Warning(f"Coundnt determine a week parsing for {week}")

    return spreadsheet.batch_update({"requests": requests})


def unmerge_cells_batch(spreadsheet, cells_data, sheet_idx):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    for (
        start_row_index,
        end_row_index,
        start_col_idx,
        end_col_idx,
    ) in cells_data:
        requests.append(
            {
                "unmergeCells": {
                    "range": {
                        "sheetId": sheet.id,
                        "startRowIndex": start_row_index,
                        "endRowIndex": end_row_index,
                        "startColumnIndex": start_col_idx,
                        "endColumnIndex": end_col_idx,
                    },
                }
            }
        )
    spreadsheet.batch_update({"requests": requests})


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


def color_cells_batch(
    spreadsheet,
    cell_data,
    sheet_idx,
):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    # to_color = zip(
    #     start_row_indexs,
    #     start_col_indexs,
    #     rgb_color,
    # )

    for start_row_index, start_col_index, rgb_color in cell_data:
        color_dict = {
            "red": rgb_color[0],
            "green": rgb_color[1],
            "blue": rgb_color[2],
        }

        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": int(sheet.id),
                        "startRowIndex": start_row_index - 1,
                        "endRowIndex": start_row_index,
                        "startColumnIndex": start_col_index,
                        "endColumnIndex": start_col_index + 1,
                    },
                    "cell": {"userEnteredFormat": {"backgroundColor": color_dict}},
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        )

    return spreadsheet.batch_update({"requests": requests})


def write_cells_batch(spreadsheet, cell_data, sheet_idx):
    """ """
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    for row_index, col_index, value in cell_data:
        value_key = "numberValue" if isinstance(value, (int, float)) else "stringValue"

        requests.append(
            {
                "updateCells": {
                    "range": {
                        "sheetId": int(sheet.id),
                        "startRowIndex": row_index - 1,
                        "endRowIndex": row_index,
                        "startColumnIndex": col_index,
                        "endColumnIndex": col_index + 1,
                    },
                    "rows": [{"values": [{"userEnteredValue": {value_key: value}}]}],
                    "fields": "userEnteredValue",
                }
            }
        )

    return spreadsheet.batch_update({"requests": requests})


def check_overlaps(cells_data):
    overlaps = []
    n = len(cells_data)

    for i in range(n):
        for j in range(i + 1, n):
            # Extraction des coordonnées pour plus de clarté
            r1_s, r1_e, c1_s, c1_e = cells_data[i]
            r2_s, r2_e, c2_s, c2_e = cells_data[j]

            # Vérification du chevauchement vertical
            overlap_row = max(r1_s, r2_s) < min(r1_e, r2_e)
            overlap_col = max(c1_s, c2_s) < min(c1_e, c2_e)

            if overlap_row and overlap_col:
                overlaps.append((cells_data[i], cells_data[j]))

    return overlaps


def get_position_from_params(start, end, week, index_sheet, data):
    """
    find the corresponding position for params in a edt_clean row
    """
    date_str = format_date(start, format="full", locale="fr_FR")
    date_position = index_sheet[date_str][0]

    times_raw = [row[0] for row in data[date_position[0] + 1 : date_position[0] + 9]]
    times_start = [time.split("\n")[0].strip() for time in times_raw]
    times_end = [time.split("\n")[1].strip() for time in times_raw]

    mapping_time_start = {v: k + date_position[0] for k, v in enumerate(times_start)}
    mapping_time_end = {v: k + date_position[0] for k, v in enumerate(times_end)}

    hour_start_str = start.strftime("%H:%M")
    hour_end_str = end.strftime("%H:%M")

    row_idx_start = mapping_time_start[hour_start_str]
    row_idx_end = mapping_time_end[hour_end_str] + 1

    if pd.isna(week):
        col_idx_start = date_position[1]
        col_idx_end = date_position[1] + 2
    elif week == "A":
        col_idx_start = date_position[1]
        col_idx_end = date_position[1] + 1
    elif week == "B":
        col_idx_start = date_position[1] + 1
        col_idx_end = date_position[1] + 2
    else:
        raise ValueError("Coudnt parse week")

    return [
        row_idx_start + 1,
        row_idx_end + 1,
        col_idx_start,
        col_idx_end,
    ]
