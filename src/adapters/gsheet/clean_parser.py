import pandas as pd
from datetime import datetime
from src.adapters.gsheet.client import GSheetClient
from src.domain.timetable import Timetable
from src.domain.models import Session
from src.domain.ports import TimetableRepository
import ast

class GSheetCleanTimetableParser(TimetableRepository):
    """Adaptateur pour lire l'emploi du temps depuis la feuille tabulaire 'edt_clean'."""

    def __init__(self, client: GSheetClient):
        self.gs_client = client

    def load(self) -> Timetable:
        spreadsheet = self.gs_client.open_spreadsheet()
        try:
            sheet = spreadsheet.worksheet("edt_clean")
        except:
            # Si elle n'existe pas, on retourne un emploi du temps vide
            return Timetable()

        data = sheet.get_all_values()
        if len(data) < 2:
            return Timetable()

        df = pd.DataFrame(data[1:], columns=data[0])
        timetable = Timetable()

        for _, row in df.iterrows():
            try:
                # Format attendu : JJ/MM/AAAA HH:mm:ss
                start_str = row.get("start")
                end_str = row.get("end")
                
                # Conversion robuste des dates
                start_dt = self._parse_date(start_str)
                end_dt = self._parse_date(end_str)
                
                if not start_dt or not end_dt:
                    continue

                # Professors (peut être une chaîne ou une liste évaluée)
                profs_raw = row.get("prof", "[]")
                try:
                    profs = ast.literal_eval(profs_raw) if profs_raw.startswith("[") else [p.strip() for p in profs_raw.split("/") if p.strip()]
                except:
                    profs = [profs_raw]

                session = Session(
                    course_name=row.get("cours", "Inconnu"),
                    start_time=start_dt,
                    end_time=end_dt,
                    professors=profs,
                    course_type=row.get("type_cours"),
                    room=row.get("salle"),
                    group=row.get("groupe_etudiant"),
                    color_rgb=row.get("color_rgb")
                )
                timetable.add_session(session)
            except Exception as e:
                print(f"Erreur parsing ligne edt_clean : {e}")
                continue

        return timetable

    def _parse_date(self, date_str):
        if not date_str: return None
        formats = ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        return None
