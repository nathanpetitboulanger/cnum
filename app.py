import streamlit as st
from src.config_loader.settings import Settings
from src.adapters.gsheet.client import GSheetClient
from src.adapters.gsheet.parser import GSheetTimetableParser
from src.adapters.gsheet.drawer import GSheetDrawer
from src.domain.stats import StatsService

def run_audit_and_update():
    settings = Settings()
    gs_client = GSheetClient(settings)
    
    st.info("Extraction des données en cours...")
    parser = GSheetTimetableParser(gs_client)
    timetable = parser.load()
    st.success(f"Extraction terminée : {len(timetable)} sessions trouvées.")
    
    st.info("Calcul des statistiques...")
    stats_service = StatsService(timetable)
    stats = stats_service.get_all_stats()
    st.success("Statistiques calculées.")
    
    st.info("Mise à jour de Google Sheets (Feuille 'drawing')...")
    drawer = GSheetDrawer(gs_client)
    drawer.render(timetable)
    st.success("Mise à jour terminée avec succès !")

st.title("CNUM - Gestionnaire d'Emploi du Temps")

if st.button("Lancer la mise à jour de l'EDT"):
    try:
        run_audit_and_update()
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
        st.exception(e)
