import gspread
from utils.fetch_data import extract_legend
import pandas as pd
from typing import Mapping


def add_col_group_to_df_with_RGB(
    df: pd.DataFrame, meta_data: Mapping, sheet_param: gspread.Worksheet
):
    cours_legend = extract_legend(meta_data, sheet_param)
    cours_legend_pd = pd.Series(cours_legend)
    df["type_cours"] = df["RGB"].map(cours_legend_pd)  # type: ignore
    return df
