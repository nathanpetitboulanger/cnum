import ast
from utils.draw_function import get_position_from_params


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
    request_ = {
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
    return request_


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

    request_ = {
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
    return request_


def get_all_requests_from_df(
    df,
    index_sheet,
    sheet_id,
    data,
) -> list:
    all_requests = []

    for k in range(len(df)):
        row_test = k
        start = df.iloc[row_test]["start"]
        end = df.iloc[row_test]["end"]
        week = df.iloc[row_test]["semaine"]
        value = df.iloc[row_test]["cours"]
        rgb_str = df.iloc[row_test]["RGB"]
        rgb = ast.literal_eval(rgb_str)

        positions = get_position_from_params(
            start,
            end,
            week,
            index_sheet,
            data,
        )

        all_requests.append(get_merge_request(sheet_id, *positions))
        all_requests.append(
            get_color_request(sheet_id, positions[0], col=positions[2], rgb=rgb)
        )
        all_requests.append(
            get_write_request(sheet_id, positions[0], positions[2], value=value)
        )
    return all_requests


def get_request_unmerge_entire_sheet(sheet):
    total_rows = sheet.row_count
    total_cols = sheet.col_count

    requests_ = [
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
    return requests_


def get_requests_reset_sheet_color(sheet):
    total_rows = sheet.row_count
    total_cols = sheet.col_count

    requests_ = [
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
    return requests_


def get_request_clear_all_values(sheet):
    """
    Génère une requête pour supprimer TOUTES les valeurs de la feuille
    tout en conservant le formatage (couleurs, bordures, etc.).
    """
    request_ = {
        "repeatCell": {
            "range": {
                "sheetId": int(sheet.id),
            },
            "cell": {},
            "fields": "userEnteredValue",
        }
    }
    return request_
