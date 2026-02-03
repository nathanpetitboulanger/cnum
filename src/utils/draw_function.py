def merge_cells_batch(
    spreadsheet, start_row_indexs, end_row_indexs, start_col_idx, end_col_idx, sheet_idx
):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    to_merge = zip(start_row_indexs, end_row_indexs, start_col_idx, end_col_idx)

    for (
        start_row_index,
        end_row_index,
        start_col_idx,
        end_col_idx,
    ) in to_merge:
        requests.append(
            {
                "mergeCells": {
                    "range": {
                        "sheetId": sheet.id,
                        "startRowIndex": start_row_index,
                        "endRowIndex": end_row_index,
                        "startColumnIndex": start_col_idx,
                        "endColumnIndex": end_col_idx,
                    },
                    "mergeType": "MERGE_ALL",
                }
            }
        )
    spreadsheet.batch_update({"requests": requests})


def unmerge_cells_batch(
    spreadsheet, start_row_indexs, end_row_indexs, start_col_idx, end_col_idx, sheet_idx
):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    to_merge = zip(start_row_indexs, end_row_indexs, start_col_idx, end_col_idx)

    for (
        start_row_index,
        end_row_index,
        start_col_idx,
        end_col_idx,
    ) in to_merge:
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
    start_row_indexs,
    start_col_indexs,
    rgb_color,
    sheet_idx,
):
    sheet = spreadsheet.get_worksheet(sheet_idx)
    requests = []

    to_color = zip(
        start_row_indexs,
        start_col_indexs,
        rgb_color,
    )

    for start_row, start_col, rgb_color in to_color:
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
                        "startRowIndex": start_row,
                        "endRowIndex": start_row + 1,
                        "startColumnIndex": start_col,
                        "endColumnIndex": start_col + 1,
                    },
                    "cell": {"userEnteredFormat": {"backgroundColor": color_dict}},
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        )

    return spreadsheet.batch_update({"requests": requests})
