import pandas as pd
from typing import Dict
from src.domain.timetable import Timetable

class StatsService:
    """
    Service expert en calculs statistiques sur un Timetable.
    Il transforme les donnees d'objets en DataFrames de synthese.
    """

    def __init__(self, timetable: Timetable):
        self.timetable = timetable
        self._df = self._to_exploded_dataframe()

    def _to_exploded_dataframe(self) -> pd.DataFrame:
        """
        Methode interne qui prepare un DataFrame 'explose' ou chaque prof
        a sa propre ligne, ce qui facilite les calculs GroupBy.
        """
        rows = []
        for s in self.timetable.sessions:
            # On cree une ligne pour chaque professeur de la session
            for prof in s.professors:
                rows.append({
                    "professor": prof,
                    "duration": s.duration_hours,
                    "type": s.course_type or "Inconnu",
                    "group": s.group or "Sans Groupe",
                    "start": s.start_time,
                    "week": s.start_time.strftime("%Y-W%V"),
                    "monday": s.start_time.date() - pd.Timedelta(days=s.start_time.weekday())
                })
        return pd.DataFrame(rows)

    def get_professor_summary(self) -> pd.DataFrame:
        """Total d'heures par professeur."""
        summary = self._df.groupby("professor")["duration"].sum().reset_index()
        summary.columns = ["Enseignant", "Total Heures"]
        return summary.sort_values(by="Total Heures", ascending=False)

    def get_weekly_professor_summary(self) -> pd.DataFrame:
        """Total d'heures par professeur et par semaine."""
        summary = self._df.groupby(["week", "monday", "professor"])["duration"].sum().reset_index()
        summary.columns = ["Semaine", "Lundi", "Enseignant", "Heures"]
        return summary.sort_values(by=["Semaine", "Heures"], ascending=[True, False])

    def get_type_summary(self) -> pd.DataFrame:
        """Total d'heures par type de cours (TD, TP, etc.)."""
        summary = self._df.groupby("type")["duration"].sum().reset_index()
        summary.columns = ["Type de Cours", "Total Heures"]
        return summary.sort_values(by="Total Heures", ascending=False)

    def get_group_summary(self) -> pd.DataFrame:
        """Total d'heures par groupe d'etudiants."""
        summary = self._df.groupby("group")["duration"].sum().reset_index()
        summary.columns = ["Groupe", "Total Heures"]
        return summary.sort_values(by="Total Heures", ascending=False)

    def get_all_stats(self) -> Dict[str, pd.DataFrame]:
        """Retourne un dictionnaire contenant tous les rapports."""
        return {
            "prof": self.get_professor_summary(),
            "week": self.get_weekly_professor_summary(),
            "type": self.get_type_summary(),
            "group": self.get_group_summary()
        }
