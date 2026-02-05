from utils.functions import get_index_sheet
from utils.buid_draw_requests import (
    get_request_unmerge_entire_sheet,
    get_requests_reset_sheet_color,
    get_request_clear_all_values,
    get_all_requests_from_df,
)


def draw_sheet_from_df(
    df,
    draw_sheet,
    edt_sheet,
    spreadsheet,
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


def draw_sheet_for_prof(df, spreadsheet, edt_sheet, prof):
    PROF = prof
    df_filtred = df.query("prof.str.contains(@PROF)")

    sheet_for_prof = spreadsheet.add_worksheet(
        title=f"EDT for {prof}",
        rows="100",
        cols="20",
    )
    draw_sheet_from_df(df_filtred, sheet_for_prof, edt_sheet, spreadsheet)

    return sheet_for_prof
