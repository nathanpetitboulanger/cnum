import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os
import sys
import traceback
import logging

# Configuration du logger pour capturer les erreurs de l'interface
logger = logging.getLogger("cnum_parser")

# Importation de notre nouvelle architecture POO
from src.core.gsheet_parser import GSheetTimetableParser
from src.core.parser import CSVTimetableParser
from src.io.gsheet_exporter import GSheetTimetableExporter
from src.io.gsheet_drawer import GSheetDrawer
from src.io.ical_exporter import ICalExporter
from src.models.timetable import Timetable

# Configuration de la page
st.set_page_config(
    page_title="CNUM Object Center",
    page_icon="💎",
    layout="wide",
)

# --- CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    .stApp {
        background-color: #020617;
        background-image: linear-gradient(rgba(14, 165, 233, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(14, 165, 233, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .gradient-text {
        background: linear-gradient(to right, #fff 20%, #0ea5e9 50%, #6366f1 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    .stCard {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .stButton > button {
        width: 100%;
        background-color: #0ea5e9 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE ---
def get_timetable():
    if 'timetable' not in st.session_state:
        st.session_state.timetable = None
    return st.session_state.timetable

# --- HEADER ---
st.markdown('<div style="text-align: center; padding: 20px 0;"><h1 class="gradient-text">CNUM Object Center</h1><p style="color: #94a3b8;">Gestion visuelle & Archivage</p></div>', unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1])

with col_main:
    try:
        # --- ACQUISITION ---
        st.markdown('<div class="stCard"><h3>📥 1. Acquisition des Données</h3>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🌐 CHARGER DEPUIS GOOGLE SHEETS"):
                with st.spinner("Parsing en cours..."):
                    parser = GSheetTimetableParser()
                    st.session_state.timetable = parser.parse()
                    st.success(f"Récupéré : {len(st.session_state.timetable)} sessions.")
        with c2:
            if st.button("📄 CHARGER DEPUIS LE CSV"):
                parser = CSVTimetableParser()
                csv_path = 'legacy/finale.csv'
                if os.path.exists(csv_path):
                    st.session_state.timetable = parser.parse(csv_path)
                    st.success(f"Chargé : {len(st.session_state.timetable)} sessions.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- VISUALISATION & DESSIN ---
        timetable = get_timetable()
        if timetable:
            st.markdown('<div class="stCard"><h3>🎨 2. Génération Visuelle</h3>', unsafe_allow_html=True)
            st.write("Cette étape va redessiner l'emploi du temps complet sur la feuille 'drawing'.")
            
            if st.button("🖌️ GÉNÉRER LA FEUILLE 'DRAWING'"):
                with st.spinner("Dessin en cours sur Google Sheets..."):
                    drawer = GSheetDrawer()
                    drawer.apply_to_main_edt(timetable)
                    st.success("Feuille 'drawing' prête !")

            st.divider()
            
            if st.button("✅ APPLIQUER À L'EDT OFFICIEL"):
                with st.spinner("Copie de 'drawing' vers 'EDT'..."):
                    drawer = GSheetDrawer()
                    drawer.commit_to_main_edt()
                    st.success("L'emploi du temps officiel a été mis à jour !")
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        # On capture l'erreur, on l'affiche proprement et on l'enregistre dans le log
        err_msg = traceback.format_exc()
        logger.error(f"STREAMLIT ERROR: {e}\n{err_msg}")
        st.error(f"Une erreur est survenue : {e}")
        with st.expander("Voir les détails techniques"):
            st.code(err_msg)

with col_side:
    st.markdown('<div class="stCard"><h3>💾 3. Exports & Sauvegardes</h3>', unsafe_allow_html=True)
    if timetable:
        if st.button("📤 MAJ DONNÉES PROPRES (TABLEAUX)"):
            with st.spinner("Mise à jour des stats..."):
                exporter = GSheetTimetableExporter()
                exporter.export_all(timetable)
                st.success("Données propres à jour !")

        st.divider()
        
        prof_list = sorted(list(timetable.teachers))
        selected_prof = st.selectbox("Enseignant :", prof_list)
        if st.button(f"Générer iCal"):
            filtered_tt = timetable.filter_by_teacher(selected_prof)
            output_file = f"edt_{selected_prof.replace(' ', '_').lower()}.ics"
            ICalExporter(calendar_name=f"EDT {selected_prof}").export(filtered_tt, output_file)
            st.success("ICS Généré")
            with open(output_file, "rb") as f:
                st.download_button("📥 Télécharger .ics", f, file_name=output_file)
    else:
        st.info("Chargez des données pour activer les exports.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align: center; color: #475569; font-size: 0.8rem; margin-top: 50px;">CNUM 2026 • Mode Diagnostic Activé</div>', unsafe_allow_html=True)
