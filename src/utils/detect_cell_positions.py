import re


def get_dates_positions_from_data(data) -> list:
    """
    Iterate on each cell, find paternes like "lundi 16 février 2026"
    and add id detected, the position row,col in a liste. Return the list
    """

    pattern_capture_date = r"^(\w+)\s+(\d{1,2})\s+(\w+)\s+(\d{4})$"
    dates_potitions = []
    for row_index, row in enumerate(data):
        for col_index, cell in enumerate(row):
            if re.match(pattern_capture_date, data[row_index][col_index]):
                dates_potitions.append([row_index, col_index])
    return dates_potitions
