import pandas as pd


def get_prof_hours_summary(df):
    """
    Prend le DF de l'EDT et retourne un résumé : Professeur | Total Heures
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Nettoyage rapide des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Séparation des professeurs (si plusieurs par ligne)
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 3. Calcul de la somme par professeur
    summary = df_exploded.groupby("prof")["delta"].sum().reset_index()
    summary.columns = ["professeur", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_total_hours_prof_by_week(df):
    """
    Retourne un DF du total d'heures par prof par semaine.
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Conversion en datetime et extraction de la semaine et du lundi
    df["start"] = pd.to_datetime(df["start"])
    df["week"] = df["start"].dt.strftime("%Y-W%V")
    df["date_lundi"] = df["start"].dt.to_period("W").dt.start_time

    # 2. Nettoyage des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 3. Séparation des professeurs
    df_exploded = (
        df.assign(prof=df["prof"].str.split(",")).explode("prof").query("prof != ''")
    )
    df_exploded["prof"] = df_exploded["prof"].str.strip()

    # 4. Calcul de la somme par semaine (et date) et par professeur
    summary = (
        df_exploded.groupby(["week", "date_lundi", "prof"])["delta"].sum().reset_index()
    )
    summary.columns = ["semaine", "date_lundi", "professeur", "total_hours"]

    return summary.sort_values(by=["semaine", "total_hours"], ascending=[True, False])


def get_type_cours_hours_summary(df):
    """
    Prend le DF de l'EDT et retourne un résumé : Type de Cours | Total Heures
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Nettoyage rapide des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Séparation des types de cours (si plusieurs par ligne)
    df_exploded = (
        df.assign(type_cours=df["type_cours"].str.split(","))
        .explode("type_cours")
        .query("type_cours != ''")
    )

    df_exploded["type_cours"] = df_exploded["type_cours"].str.strip()

    # 3. Calcul de la somme par type de cours
    summary = df_exploded.groupby("type_cours")["delta"].sum().reset_index()
    summary.columns = ["type_cours", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)


def get_group_etudiant_hours_summary(df):
    """
    Prend le DF de l'EDT et retourne un résumé : Groupe Étudiant | Total Heures
    """
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # 1. Nettoyage rapide des heures
    df["delta"] = pd.to_numeric(
        df["delta"].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0)  # type: ignore

    # 2. Séparation des groupes (si plusieurs par ligne)
    df_exploded = (
        df.assign(groupe_etudiant=df["groupe_etudiant"].str.split(","))
        .explode("groupe_etudiant")
        .query("groupe_etudiant != ''")
    )
    df_exploded.groupe_etudiant.unique()

    df_exploded["groupe_etudiant"] = df_exploded["groupe_etudiant"].str.strip()

    # 3. Calcul de la somme par groupe
    summary = df_exploded.groupby("groupe_etudiant")["delta"].sum().reset_index()
    summary.columns = ["groupe_etudiant", "total_hours"]

    return summary.sort_values(by="total_hours", ascending=False)
