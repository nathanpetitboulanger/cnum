import streamlit as st
import subprocess

# Configuration de la page
st.set_page_config(
    page_title="CNUM Control Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS pour matcher la vibe "tech" du site web
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    /* Background and Grid Effect */
    .stApp {
        background-color: #020617;
        background-image: 
            linear-gradient(rgba(14, 165, 233, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14, 165, 233, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* Titles and Text - Cible plus précise */
    .stApp, h1, h2, h3, .stMarkdown, [data-testid="stMarkdownContainer"] p {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" !important;
    }
    
    h1, h2, h3 {
        color: #f8fafc !important;
    }

    /* EMPÊCHE LES ICÔNES DE DEVENIR DU TEXTE */
    /* On cible les éléments qui utilisent des ligatures Material Icons */
    span:contains("_"), [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Outlined' !important;
    }

    .gradient-text {
        background: linear-gradient(to right, #fff 20%, #0ea5e9 50%, #6366f1 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
        background: linear-gradient(to right, #fff 20%, #0ea5e9 50%, #6366f1 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Cards/Containers */
    .stCard {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #0ea5e9 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        background-color: #0284c7 !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3);
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Success/Progress messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        color: #10b981 !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def run_cmd(cmd):
    try:
        with st.spinner(f"Exécution : {' '.join(cmd)}"):
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                st.success(f"Commande réussie : {' '.join(cmd)}")
                if result.stdout:
                    with st.expander("Voir la sortie"):
                        st.code(result.stdout)
            else:
                st.error(f"Erreur lors de l'exécution : {' '.join(cmd)}")
                st.code(result.stderr)
    except Exception as e:
        st.error(f"Erreur système : {e}")


# Header
st.markdown(
    """
    <div style="text-align: center; padding: 40px 0;">
        <h1 class="gradient-text" style="font-size: 3rem; margin-bottom: 10px;">CNUM Control Center</h1>
        <p style="color: #94a3b8; font-weight: 500;">Interface de pilotage du backend de l'Emploi du Temps SEABV</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown(
        '<div class="stCard"><h3>⚡ Action Globale</h3>', unsafe_allow_html=True
    )
    if st.button("🚀 LANCER LE PROCESSUS COMPLET (DEMO.PY)"):
        run_cmd(["uv", "run", "src/scripts/parse_edt.py"])
        run_cmd(["uv", "run", "src/scripts/draw_df.py"])
        run_cmd(["uv", "run", "src/calcul/draw_stat_sheet.py"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="stCard"><h3>🛠️ Étapes Individuelles</h3>', unsafe_allow_html=True
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("1. 🔍 PARSER L'EDT"):
            run_cmd(["uv", "run", "src/scripts/parse_edt.py"])
        if st.button("3. 📊 CALCULER LES STATS"):
            run_cmd(["uv", "run", "src/calcul/draw_stat_sheet.py"])
    with c2:
        if st.button("2. 📅 MAJ VUE CALENDRIER"):
            run_cmd(["uv", "run", "src/scripts/draw_df.py"])
        if st.button("6. ✍️ APPLIQUER EDT"):
            run_cmd(["uv", "run", "src/scripts/apply_drawing.py"])
    st.markdown("</div>", unsafe_allow_html=True)

with col_side:
    st.markdown(
        '<div class="stCard"><h3>👤 Vues Enseignants</h3>', unsafe_allow_html=True
    )

    if st.button("📅 EDT Marc Lang"):
        run_cmd(["uv", "run", "src/scripts/display_prof_edt.py", "--prof", "Marc Lang"])

    if st.button("📅 EDT Séraphine Grellier"):
        run_cmd(
            [
                "uv",
                "run",
                "src/scripts/display_prof_edt.py",
                "--prof",
                "Séraphine Grellier",
            ]
        )

    st.divider()

    prof_nom = st.text_input("Nom de l'intervenant :", "Marc Lang")
    if st.button(f"Générer pour {prof_nom}"):
        run_cmd(["uv", "run", "src/scripts/display_prof_edt.py", "--prof", prof_nom])

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; padding: 20px; color: #475569; font-size: 0.8rem; margin-top: 50px;">
        PROJET CNUM 2026 • ENSAT • Propulsé par Python & UV
    </div>
    """,
    unsafe_allow_html=True,
)

