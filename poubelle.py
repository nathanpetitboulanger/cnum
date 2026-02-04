from datetime import datetime
from pickle import TRUE
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def check_overlap():
    """
    Description
    """

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
    sheet = spreadsheet.get_worksheet(5)
    data = sheet.get_all_values()

    df = pd.DataFrame(columns=data[0], data=data[1:])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    objet_semaine = ["A", "B"]

    for lettre in objet_semaine:
        exclusion = "B" if lettre == "A" else "A"
        df_week = df.query("semaine not in [@exclusion]").sort_values("start")
        conflicts = df_week["end"] > df_week["start"].shift(-1)

        if conflicts.any():
            raise ValueError(f"Overlapping error")

    print("Success")
    return True


check_overlap()
