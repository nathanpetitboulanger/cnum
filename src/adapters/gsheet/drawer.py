import gspread
import ast
from typing import List, Dict
from src.adapters.gsheet.client import GSheetClient
from src.domain.timetable import Timetable
from src.domain.ports import TimetableRenderer
from src.utils.functions import (
    get_index_sheet,
    get_dates_positions_from_data,
    get_position_from_params,
    get_all_merges
)

class GSheetDrawer(TimetableRenderer):
    """Adaptateur pour dessiner l'emploi du temps sur Google Sheets."""

    def __init__(self, client: GSheetClient):
        self.gs_client = client

    def render(self, timetable: Timetable):
        """Méthode principale de l'interface TimetableRenderer."""
        self.apply_to_main_edt(timetable)

    def apply_to_main_edt(self, timetable: Timetable):
        spreadsheet = self.gs_client.open_spreadsheet()
        edt_sheet = spreadsheet.worksheet("EDT")

        try:
            draw_sheet = spreadsheet.worksheet("drawing")
            spreadsheet.del_worksheet(draw_sheet)
        except gspread.WorksheetNotFound:
            pass

        draw_sheet = spreadsheet.duplicate_sheet(edt_sheet.id, new_sheet_name="drawing")
        
        # Récupère les fusions EXACTES de la nouvelle feuille
        all_merges = get_all_merges(draw_sheet)
        print(f"[DEBUG] {len(all_merges)} fusions trouvées sur 'drawing' à supprimer.")
        
        self._clear_all_merges(draw_sheet, all_merges)

        self._draw_timetable(draw_sheet, edt_sheet, timetable)
        print("[SUCCESS] Feuille 'drawing' générée.")

    def _clear_all_merges(self, sheet, merges):
        """Supprime absolument toutes les fusions et blanchit les zones de cours."""
        requests = []
        
        if merges:
            for m in merges:
                requests.append({"unmergeCells": {"range": m}})

        # Blanchiment des zones de cours
        data = sheet.get_all_values()
        date_positions = get_dates_positions_from_data(data)
        for pos in date_positions:
            r, c = pos[0] + 1, pos[1]
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet.id,
                        "startRowIndex": r, "endRowIndex": r + 8,
                        "startColumnIndex": c, "endColumnIndex": c + 2,
                    },
                    "cell": {
                        "userEnteredValue": {},
                        "userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}
                    },
                    "fields": "userEnteredValue,userEnteredFormat.backgroundColor",
                }
            })

        if requests:
            self.gs_client.open_spreadsheet().batch_update({"requests": requests})

    def _draw_timetable(self, target_sheet, ref_sheet, timetable: Timetable):
        data_ref = ref_sheet.get_all_values()
        index_sheet = get_index_sheet(ref_sheet)
        requests = []
        
        # Grille d'occupation par cellule individuelle (row, col)
        occupied_cells = set()

        for s in timetable.sessions:
            try:
                group = s.group if s.group in ["A", "B"] else ""
                pos = get_position_from_params(s.start_time, s.end_time, group, index_sheet, data_ref)
                if not pos: continue
                
                # Vérification de chevauchement cellule par cellule
                # pos = [start_row, end_row, start_col, end_col]
                current_session_cells = set()
                conflict = False
                for r in range(pos[0], pos[1]):
                    for c in range(pos[2], pos[3]):
                        if (r, c) in occupied_cells:
                            conflict = True
                            break
                        current_session_cells.add((r, c))
                    if conflict: break
                
                if conflict:
                    print(f"[DEBUG] Session ignorée car chevauchement partiel détecté : {s.course_name} @ {pos}")
                    continue
                
                # Marquer les cellules comme occupées
                occupied_cells.update(current_session_cells)

                requests.append({
                    "mergeCells": {
                        "range": {
                            "sheetId": target_sheet.id,
                            "startRowIndex": pos[0], "endRowIndex": pos[1],
                            "startColumnIndex": pos[2], "endColumnIndex": pos[3],
                        },
                        "mergeType": "MERGE_ALL",
                    }
                })

                rgb = ast.literal_eval(s.color_rgb) if s.color_rgb else [1, 1, 1]
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": target_sheet.id,
                            "startRowIndex": pos[0], "endRowIndex": pos[0] + 1,
                            "startColumnIndex": pos[2], "endColumnIndex": pos[2] + 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {"red": rgb[0], "green": rgb[1], "blue": rgb[2]},
                                "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP",
                            },
                            "userEnteredValue": {"stringValue": s.course_name}
                        },
                        "fields": "userEnteredFormat,userEnteredValue",
                    }
                })
            except Exception: continue
            
        if requests:
            self.gs_client.open_spreadsheet().batch_update({"requests": requests})
