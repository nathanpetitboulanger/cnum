import pandas as pd
from src.adapters.gsheet.client import GSheetClient
from src.domain.timetable import Timetable

class GSheetCleanExporter:
    """Expert pour remplir la feuille 'edt_clean' à partir d'un Timetable."""

    def __init__(self, client: GSheetClient):
        self.gs_client = client

    def export(self, timetable: Timetable):
        spreadsheet = self.gs_client.open_spreadsheet()
        
        # 1. Vérifier/Créer la feuille
        try:
            sheet = spreadsheet.worksheet("edt_clean")
        except:
            sheet = spreadsheet.add_worksheet(title="edt_clean", rows="100", cols="20")

        # 2. Préparer les données
        rows = []
        for s in timetable.sessions:
            rows.append({
                "start": s.start_time.strftime("%d/%m/%Y %H:%M:%S"),
                "end": s.end_time.strftime("%d/%m/%Y %H:%M:%S"),
                "cours": s.course_name,
                "prof": str(s.professors),
                "type_cours": s.course_type or "",
                "salle": s.room or "",
                "groupe_etudiant": s.group or "",
                "color_rgb": s.color_rgb or ""
            })
        
        df = pd.DataFrame(rows)
        
        # 3. Écrire dans la feuille
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"[SUCCESS] {len(rows)} sessions exportées vers 'edt_clean'.")
