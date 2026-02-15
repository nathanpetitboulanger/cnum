import logging
from typing import Tuple
from src.adapters.gsheet.client import GSheetClient
from src.domain.timetable import Timetable
from src.domain.models import Session
from src.domain.ports import TimetableRepository
from src.utils.functions import (
    get_all_merges,
    get_time_delta_from_merge,
    get_text_from_merged_cell,
    parse_profs,
    clean_cours_name,
    extract_rgb_form_merge,
    parse_room,
    parse_type_cours
)
from src.utils.fetch_data import get_mapping_dict_for_name, get_mapping_dict_for_group_color

logger = logging.getLogger("cnum_parser")

class GSheetTimetableParser(TimetableRepository):
    """Adaptateur pour extraire l'emploi du temps depuis Google Sheets."""

    def __init__(self, client: GSheetClient):
        self.gs_client = client
        self._name_mapping = None
        self._group_mapping = None

    def _load_mappings(self, spreadsheet):
        if self._name_mapping is None:
            self._name_mapping = get_mapping_dict_for_name(spreadsheet)
            self._group_mapping = get_mapping_dict_for_group_color(spreadsheet)

    def load(self) -> Timetable:
        """Implémentation du port TimetableRepository."""
        spreadsheet = self.gs_client.open_spreadsheet()
        self._load_mappings(spreadsheet)
        
        sheet = spreadsheet.worksheet("EDT")
        data = sheet.get_all_values()
        all_merges = get_all_merges(sheet)
        
        params = {"fields": "sheets(data(rowData(values(effectiveFormat(backgroundColorStyle)))))"}
        metadata = spreadsheet.fetch_sheet_metadata(params=params)
        
        timetable = Timetable()
        
        for merge in all_merges:
            try:
                delta_times = get_time_delta_from_merge(data, merge)
                if delta_times[0] is None: continue
                    
                raw_text = get_text_from_merged_cell(data, merge)
                if not raw_text.strip(): continue
                
                course_name = clean_cours_name(raw_text)
                prof_initials = parse_profs(raw_text)
                prof_names = [self._name_mapping.get(init, init) for init in prof_initials]
                
                rgb = extract_rgb_form_merge(metadata, merge)
                group = self._group_mapping.get(str(rgb))
                
                session = Session(
                    course_name=course_name,
                    start_time=delta_times[0],
                    end_time=delta_times[1],
                    professors=prof_names,
                    course_type=parse_type_cours(raw_text),
                    room=parse_room(raw_text),
                    group=group,
                    color_rgb=str(rgb)
                )
                timetable.add_session(session)

            except Exception as e:
                logger.error(f"Erreur lors du traitement d'un bloc : {e}")
                continue

        return timetable
