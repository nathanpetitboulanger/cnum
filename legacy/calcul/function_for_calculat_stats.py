import pandas as pd


def get_prof_hours_summary(df):
    """
    Takes the timetable DF and returns a summary: Professor | Total Hours
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Quick hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Separate professors (if multiple per row)
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 3. Calculate sum per professor
    summary = df_exploded.groupby("prof")["delta"].sum().reset_index()
    summary.columns = ["professor", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_total_hours_prof_by_week(df):
    """
    Returns a DF of total hours per professor per week.
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Convert to datetime and extract week and Monday
    df["start"] = pd.to_datetime(df["start"])
    df["week"] = df["start"].dt.strftime("%Y-W%V")
    df["monday_date"] = df["start"].dt.to_period("W").dt.start_time

    # 2. Hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 3. Separate professors
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 4. Calculate sum per week (and date) and per professor
    summary = (
        df_exploded.groupby(["week", "monday_date", "prof"])["delta"].sum().reset_index()
    )
    summary.columns = ["week", "monday_date", "professor", "total_hours"]

    return summary.sort_values(by=["week", "total_hours"], ascending=[True, False])


def get_type_cours_hours_summary(df):
    """
    Takes the timetable DF and returns a summary: Course Type | Total Hours
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Quick hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Separate course types (if multiple per row)
    df_exploded = (
        df.assign(type_cours=df["type_cours"].str.split(","))
        .explode("type_cours")
        .query("type_cours != ''")
    )

    df_exploded["type_cours"] = df_exploded["type_cours"].str.strip()

    # 3. Calculate sum per course type
    summary = df_exploded.groupby("type_cours")["delta"].sum().reset_index()
    summary.columns = ["course_type", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_total_hours_type_cours_by_week(df):
    """
    Returns a DF of total hours per course type per week.
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Convert to datetime and extract week and Monday
    df["start"] = pd.to_datetime(df["start"])
    df["week"] = df["start"].dt.strftime("%Y-W%V")
    df["monday_date"] = df["start"].dt.to_period("W").dt.start_time

    # 2. Hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 3. Separate course types
    df_exploded = (
        df.assign(type_cours=df["type_cours"].str.split(","))
        .explode("type_cours")
        .query("type_cours != ''")
    )
    df_exploded["type_cours"] = df_exploded["type_cours"].str.strip()

    # 4. Calculate sum per week (and date) and per course type
    summary = (
        df_exploded.groupby(["week", "monday_date", "type_cours"])["delta"]
        .sum()
        .reset_index()
    )
    summary.columns = ["week", "monday_date", "course_type", "total_hours"]

    return summary.sort_values(by=["week", "total_hours"], ascending=[True, False])


def get_group_etudiant_hours_summary(df):
    """
    Takes the timetable DF and returns a summary: Student Group | Total Hours
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Quick hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Separate groups (if multiple per row)
    df_exploded = (
        df.assign(groupe_etudiant=df["groupe_etudiant"].str.split(","))
        .explode("groupe_etudiant")
        .query("groupe_etudiant != ''")
    )

    df_exploded["groupe_etudiant"] = df_exploded["groupe_etudiant"].str.strip()

    # 3. Calculate sum per group
    summary = df_exploded.groupby("groupe_etudiant")["delta"].sum().reset_index()
    summary.columns = ["student_group", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_total_hours_group_etudiant_by_week(df):
    """
    Returns a DF of total hours per student group per week.
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Convert to datetime and extract week and Monday
    df["start"] = pd.to_datetime(df["start"])
    df["week"] = df["start"].dt.strftime("%Y-W%V")
    df["monday_date"] = df["start"].dt.to_period("W").dt.start_time

    # 2. Hours cleaning
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 3. Separate groups
    df_exploded = (
        df.assign(groupe_etudiant=df["groupe_etudiant"].str.split(","))
        .explode("groupe_etudiant")
        .query("groupe_etudiant != ''")
    )
    df_exploded["groupe_etudiant"] = df_exploded["groupe_etudiant"].str.strip()

    # 4. Calculate sum per week (and date) and per group
    summary = (
        df_exploded.groupby(["week", "monday_date", "groupe_etudiant"])["delta"]
        .sum()
        .reset_index()
    )
    summary.columns = ["week", "monday_date", "student_group", "total_hours"]

    return summary.sort_values(by=["week", "total_hours"], ascending=[True, False])