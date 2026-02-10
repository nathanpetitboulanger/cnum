import pandas as pd
import ast
from utils.fetch_data import get_df_from_sheet_index


df = get_df_from_sheet_index(3)


def calculate_sum_hours(df):
    df["delta"] = df["delta"].astype(str).str.replace(",", ".").astype(float)
    stats = df.groupby("type_cours")["delta"].sum()
    return stats


prof = "Benjamin Pey"


def get_prof_total_hours(df: pd.DataFrame, prof: str):
    """
    return the sum of total hours
    """
    df["delta"] = df["delta"].astype(str).str.replace(",", ".").astype(float)
    df_filterd = df.query("prof.str.contains(@prof)")
    sum_h = df_filterd["delta"].sum()
    return sum_h


def calculate_all_profs_stats(df: pd.DataFrame):
    """
    Return a dataframe with the sum of hours for all profs
    """
    df = df.loc[:, ~df.columns.duplicated()]
    df["delta"] = df["delta"].astype(str).str.replace(",", ".").astype(float)

    # Split by comma and explode
    df_exploded = df.assign(prof=df["prof"].str.split(",")).explode("prof")

    # Strip whitespace
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # Filter out empty strings
    df_exploded = df_exploded[df_exploded["prof"] != ""]

    # Remove duplicates per original row to avoid double counting within the same cell
    # Reset index to include the original row index in the duplicate check
    df_exploded = df_exploded.reset_index().drop_duplicates()

    # Group and sum
    stats = (
        df_exploded.groupby("prof")["delta"]
        .sum()
        .reset_index()
        .sort_values(by="delta", ascending=False)
    )
    return stats


if __name__ == "__main__":
    print(calculate_all_profs_stats(df))
