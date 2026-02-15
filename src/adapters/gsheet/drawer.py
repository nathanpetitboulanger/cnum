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

    def create_professor_preview(self, timetable: Timetable, prof_name: str):
        """Génère une feuille où seuls les cours du prof sont en couleur, le reste est grisé."""
        spreadsheet = self.gs_client.open_spreadsheet()
        edt_sheet = spreadsheet.worksheet("EDT")
        
        sheet_name = f"Preview {prof_name}"
        try:
            prof_sheet = spreadsheet.worksheet(sheet_name)
            spreadsheet.del_worksheet(prof_sheet)
        except gspread.WorksheetNotFound:
            pass

        prof_sheet = spreadsheet.duplicate_sheet(edt_sheet.id, new_sheet_name=sheet_name)
        
        # 1. On nettoie les fusions existantes
        all_merges = get_all_merges(prof_sheet)
        self._clear_all_merges(prof_sheet, all_merges)
        
        # 2. On grise toute la zone de l'EDT
        self._grey_out_area(prof_sheet)
        
        # 3. On dessine uniquement les cours du prof
        prof_timetable = timetable.filter_by_teacher(prof_name)
        self._draw_timetable(prof_sheet, edt_sheet, prof_timetable)
        print(f"[SUCCESS] Feuille '{sheet_name}' générée.")

    def _grey_out_area(self, sheet):
        """Applique un fond gris clair sur toutes les zones de cours."""
        data = sheet.get_all_values()
        date_positions = get_dates_positions_from_data(data)
        requests = []
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
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor",
                }
            })
        if requests:
            self.gs_client.open_spreadsheet().batch_update({"requests": requests})

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
        spreadsheet = self.gs_client.open_spreadsheet()
        from src.utils.fetch_data import get_mapping_dict_for_name
        
        # On récupère le mapping pour pouvoir transformer Nom Complet -> Initiales
        # On utilise try/except au cas où l'onglet Paramètres serait inaccessible
        try:
            name_to_init = {v: k for k, v in get_mapping_dict_for_name(spreadsheet).items()}
        except:
            name_to_init = {}

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

                # Gestion robuste de la couleur
                try:
                    if s.color_rgb and isinstance(s.color_rgb, str):
                        clean_color = s.color_rgb.replace("(", "").replace(")", "")
                        rgb_values = [float(x.strip()) for x in clean_color.split(",")]
                        rgb = {"red": rgb_values[0], "green": rgb_values[1], "blue": rgb_values[2]}
                    else:
                        rgb = {"red": 1, "green": 1, "blue": 1}
                except Exception:
                    rgb = {"red": 1, "green": 1, "blue": 1}

                # Composition du texte selon les règles : (INIT) [SALLE] "TYPE"
                # On repasse des noms complets aux initiales pour le visuel
                inits = [name_to_init.get(p, p) for p in s.professors]
                prof_str = f"({ '/'.join(inits) })" if inits else ""
                salle_str = f"[{s.room}]" if s.room else ""
                type_str = f'"{s.course_type}"' if s.course_type else ""
                
                display_text = f"{s.course_name}\n{prof_str} {salle_str} {type_str}".strip()

                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": target_sheet.id,
                            "startRowIndex": pos[0], "endRowIndex": pos[1],
                            "startColumnIndex": pos[2], "endColumnIndex": pos[3],
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": rgb,
                                "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP",
                                "textFormat": {"fontSize": 9}
                            },
                            "userEnteredValue": {"stringValue": display_text}
                        },
                        "fields": "userEnteredFormat,userEnteredValue",
                    }
                })
            except Exception: continue
            
        if requests:
            self.gs_client.open_spreadsheet().batch_update({"requests": requests})
