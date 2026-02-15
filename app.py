import streamlit as st
import pandas as pd
from src.config_loader.settings import Settings
from src.adapters.gsheet.client import GSheetClient
from src.adapters.gsheet.parser import GSheetTimetableParser
from src.adapters.gsheet.drawer import GSheetDrawer
from src.domain.stats import StatsService

st.set_page_config(page_title="CNUM - ENSAT", layout="wide")
st.title("CNUM - Gestionnaire d'Emploi du Temps")

# Initialisation persistante dans la session Streamlit
if 'timetable' not in st.session_state:
    st.session_state.timetable = None

settings = Settings()
gs_client = GSheetClient(settings)

col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Extraction")
    if st.button("Extraire l'EDT depuis Google Sheets"):
        try:
            parser = GSheetTimetableParser(gs_client)
            st.session_state.timetable = parser.load()
            st.success(f"{len(st.session_state.timetable)} sessions extraites.")
        except Exception as e:
            st.error(f"Erreur extraction : {e}")

with col2:
    st.header("2. Statistiques")
    if st.session_state.timetable:
        if st.button("Calculer les statistiques"):
            try:
                stats_service = StatsService(st.session_state.timetable)
                stats = stats_service.get_all_stats()
                st.session_state.stats = stats
                st.success("Stats calculées.")
            except Exception as e:
                st.error(f"Erreur stats : {e}")
    else:
        st.info("Extraire l'EDT d'abord.")

with col3:
    st.header("3. Rendu")
    if st.session_state.timetable:
        if st.button("Générer la feuille 'drawing'"):
            try:
                drawer = GSheetDrawer(gs_client)
                drawer.render(st.session_state.timetable)
                st.success("Feuille 'drawing' mise à jour !")
            except Exception as e:
                st.error(f"Erreur rendu : {e}")
        
        st.divider()
        st.subheader("Prévisu Professeur")
        # Récupération de la liste des profs unique
        prof_list = sorted(list(st.session_state.timetable.teachers))
        selected_prof = st.selectbox("Choisir un enseignant", prof_list)
        
        if st.button(f"Générer l'EDT de {selected_prof}"):
            try:
                drawer = GSheetDrawer(gs_client)
                # Utilisation explicite de st.session_state.timetable
                drawer.create_professor_preview(st.session_state.timetable, selected_prof)
                st.success(f"Feuille 'Preview {selected_prof}' créée !")
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.info("Extraire l'EDT d'abord.")

# Affichage des stats si disponibles
if 'stats' in st.session_state:
    st.divider()
    st.subheader("Synthèse des Heures")
    tab1, tab2, tab3 = st.tabs(["Par Enseignant", "Par Semaine", "Par Type"])
    with tab1:
        st.dataframe(st.session_state.stats['prof'], use_container_width=True)
    with tab2:
        st.dataframe(st.session_state.stats['week'], use_container_width=True)
    with tab3:
        st.dataframe(st.session_state.stats['type'], use_container_width=True)
