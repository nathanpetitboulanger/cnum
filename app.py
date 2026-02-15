import streamlit as st
import pandas as pd
from src.config_loader.settings import Settings
from src.adapters.gsheet.client import GSheetClient
from src.adapters.gsheet.parser import GSheetTimetableParser
from src.adapters.gsheet.clean_parser import GSheetCleanTimetableParser
from src.adapters.gsheet.exporter import GSheetCleanExporter
from src.adapters.gsheet.drawer import GSheetDrawer
from src.domain.stats import StatsService

st.set_page_config(page_title="CNUM - ENSAT", layout="wide")
st.title("CNUM - Gestionnaire d'Emploi du Temps")

if 'timetable' not in st.session_state:
    st.session_state.timetable = None

settings = Settings()
gs_client = GSheetClient(settings)

col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Extraction & Sync")
    
    # Action Unifiée : Extraction -> Sync edt_clean -> Charge en mémoire
    if st.button("🔄 Parser l'EDT Brut & Sync"):
        try:
            with st.spinner("Extraction et mise à jour de edt_clean..."):
                # 1. Extraction depuis l'onglet brut
                parser = GSheetTimetableParser(gs_client)
                extracted_timetable = parser.load()
                
                # 2. Mise à jour automatique de la feuille 'edt_clean'
                exporter = GSheetCleanExporter(gs_client)
                exporter.export(extracted_timetable)
                
                # 3. Chargement immédiat en mémoire pour l'app
                st.session_state.timetable = extracted_timetable
                
                st.success(f"EDT Brut parsé et synchronisé vers 'edt_clean' ({len(st.session_state.timetable)} cours).")
        except Exception as e:
            st.error(f"Erreur lors du parsing : {e}")

    st.divider()
    
    # Option pour charger uniquement depuis le format tabulaire (si l'utilisateur a fait des modifs manuelles)
    if st.button("📂 Charger depuis 'edt_clean'"):
        try:
            parser = GSheetCleanTimetableParser(gs_client)
            st.session_state.timetable = parser.load()
            st.success(f"{len(st.session_state.timetable)} cours chargés depuis 'edt_clean'.")
        except Exception as e:
            st.error(f"Erreur chargement edt_clean : {e}")

with col2:
    st.header("2. Statistiques")
    if st.session_state.timetable:
        if st.button("📊 Calculer les statistiques"):
            try:
                stats_service = StatsService(st.session_state.timetable)
                stats = stats_service.get_all_stats()
                st.session_state.stats = stats
                st.success("Statistiques prêtes.")
            except Exception as e:
                st.error(f"Erreur stats : {e}")
    else:
        st.info("Extraire ou charger des données d'abord.")

with col3:
    st.header("3. Rendu Visuel")
    if st.session_state.timetable:
        if st.button("🎨 Générer la feuille 'drawing'"):
            try:
                drawer = GSheetDrawer(gs_client)
                drawer.render(st.session_state.timetable)
                st.success("Onglet 'drawing' mis à jour !")
            except Exception as e:
                st.error(f"Erreur rendu : {e}")
        
        st.divider()
        st.subheader("Fiche Enseignant")
        prof_list = sorted(list(st.session_state.timetable.teachers))
        selected_prof = st.selectbox("Sélectionner un enseignant", prof_list)
        
        if st.button(f"Générer l'EDT de {selected_prof}"):
            try:
                drawer = GSheetDrawer(gs_client)
                drawer.create_professor_preview(st.session_state.timetable, selected_prof)
                st.success(f"Feuille 'Preview {selected_prof}' créée !")
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.info("Données requises pour le rendu.")

if 'stats' in st.session_state:
    st.divider()
    st.subheader("Récapitulatif des Heures")
    tab1, tab2, tab3 = st.tabs(["Enseignants", "Hebdomadaire", "Types de cours"])
    with tab1:
        st.dataframe(st.session_state.stats['prof'], use_container_width=True)
    with tab2:
        st.dataframe(st.session_state.stats['week'], use_container_width=True)
    with tab3:
        st.dataframe(st.session_state.stats['type'], use_container_width=True)
