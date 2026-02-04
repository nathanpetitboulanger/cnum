def get_merge_request(
    sheet_id,
    start_row_index,
    end_row_index,
    start_col_index,
    end_col_index,
):
    requests_ = {
        "mergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_index,
                "endRowIndex": end_row_index,
                "startColumnIndex": start_col_index,
                "endColumnIndex": end_col_index,
            },
            "mergeType": "MERGE_ALL",
        }
    }
    return requests_


def get_color_request(sheet_id, row, col, rgb):
    request = {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": col,
                "endColumnIndex": col + 1,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": rgb[0], "green": rgb[1], "blue": rgb[2]}
                }
            },
            "fields": "userEnteredFormat.backgroundColor",
        }
    }
    return request


def get_write_request(sheet_id, row, col, value):
    """ """
    if isinstance(value, bool):
        value_key = "boolValue"
    elif isinstance(value, (int, float)):
        value_key = "numberValue"
    elif isinstance(value, str):
        if value.startswith("="):  # Si c'est une formule
            value_key = "formulaValue"
        else:
            value_key = "stringValue"
    else:
        value_key = "stringValue"

    request = {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": col,
                "endColumnIndex": col + 1,
            },
            "cell": {"userEnteredValue": {value_key: value}},
            "fields": "userEnteredValue",  # On précise qu'on ne change que la valeur
        }
    }
    return request
