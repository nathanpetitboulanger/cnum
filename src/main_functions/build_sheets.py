from utils.functions import get_index_sheet
from utils.buid_draw_requests import (
    get_request_unmerge_entire_sheet,
    get_requests_reset_sheet_color,
    get_request_clear_all_values,
    get_all_requests_from_df,
    get_request_for_reset_cells,
    get_request_for_grey_cells,
)
import gspread
from pandas import DataFrame
from utils.detect_cell_positions import get_dates_positions_from_data


def draw_sheet_from_df(
    df,
    draw_sheet: gspread.Worksheet,
    edt_sheet: gspread.Worksheet,
    spreadsheet: gspread.Spreadsheet,
):
    """
    this functions draw the dataframe content in the sheet
    """

    data_edt = edt_sheet.get_all_values()
    index_edt = get_index_sheet(edt_sheet)

    requests_ = []

    requests_.append(get_request_unmerge_entire_sheet(draw_sheet))
    requests_.append(get_requests_reset_sheet_color(draw_sheet))
    requests_.append(get_request_clear_all_values(draw_sheet))

    requests_.extend(
        get_all_requests_from_df(
            df,
            index_edt,
            draw_sheet.id,
            data_edt,
        )
    )
    spreadsheet.batch_update({"requests": requests_})


def draw_sheet_for_prof(
    df: DataFrame,
    spreadsheet: gspread.Spreadsheet,
    edt_sheet: gspread.Worksheet,
    prof: str,
):
    PROF = prof
    df_filtred = df.query("prof.str.contains(@PROF)")

    sheet_for_prof = spreadsheet.add_worksheet(
        title=f"EDT for {prof}",
        rows="100",  # type: ignore
        cols="20",  # type: ignore
    )
    draw_sheet_from_df(df_filtred, sheet_for_prof, edt_sheet, spreadsheet)

    return sheet_for_prof


def delete_cours_in_edt(
    spreadsheet: gspread.Spreadsheet,
    sheet: gspread.Worksheet,
):
    """ """
    data = sheet.get_all_values()
    dates_positions = get_dates_positions_from_data(data)

    all_requests = []

    for position in dates_positions:
        position[0] = position[0] + 1

        requests_ = get_request_for_reset_cells(
            sheet,
            *position,
            nrows=8,
            ncols=2,
        )
        all_requests.extend(requests_)

    spreadsheet.batch_update({"requests": all_requests})


def grey_out_cours_in_edt(
    spreadsheet: gspread.Spreadsheet,
    sheet: gspread.Worksheet,
):
    """ """
    data = sheet.get_all_values()
    dates_positions = get_dates_positions_from_data(data)

    all_requests = []

    for position in dates_positions:
        position[0] = position[0] + 1

        requests_ = get_request_for_grey_cells(
            sheet,
            *position,
            nrows=8,
            ncols=2,
        )
        all_requests.extend(requests_)

    spreadsheet.batch_update({"requests": all_requests})


def create_preview_edt_prof(
    spreadsheet: gspread.Spreadsheet,
    edt_sheet: gspread.Worksheet,
    df: DataFrame,
    prof: str,
):
    # 1. Duplicate EDT sheet
    new_sheet = spreadsheet.duplicate_sheet(
        edt_sheet.id,
        new_sheet_name=f"Preview {prof}",
        insert_sheet_index=100,
    )

    # 2. Delete courses to get skeleton
    delete_cours_in_edt(spreadsheet, new_sheet)

    # 3. Draw prof courses
    PROF = prof
    df_filtred = df.query("prof.str.contains(@PROF)")

    index_edt = get_index_sheet(edt_sheet)
    data_edt = edt_sheet.get_all_values()

    requests_ = get_all_requests_from_df(
        df_filtred,
        index_edt,
        new_sheet.id,
        data_edt,
    )
    spreadsheet.batch_update({"requests": requests_})

    return new_sheet
