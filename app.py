import streamlit as st
import subprocess

st.title("App de pilotage du backend de l'EDT")


def run_cmd(cmd):
    with st.spinner(f"Running: {' '.join(cmd)}"):
        subprocess.run(cmd)
    st.success("Done!")


if st.button("Lancer tout le processus (demo.py)"):
    run_cmd(["uv", "run", "src/scripts/parse_edt.py"])
    run_cmd(["uv", "run", "src/scripts/draw_df.py"])
    run_cmd(["uv", "run", "src/calcul/draw_stat_sheet.py"])
    run_cmd(["uv", "run", "src/scripts/display_prof_edt.py", "--prof", "Marc Lang"])
    run_cmd(
        ["uv", "run", "src/scripts/display_prof_edt.py", "--prof", "Séraphine Grellier"]
    )


if st.button("1. Parser l'EDT"):
    run_cmd(["uv", "run", "src/scripts/parse_edt.py"])

if st.button("2. Mettre à jour la vue calendrier"):
    run_cmd(["uv", "run", "src/scripts/draw_df.py"])

if st.button("3. Calculer les statistiques"):
    run_cmd(["uv", "run", "src/calcul/draw_stat_sheet.py"])

if st.button("4. EDT Marc Lang"):
    run_cmd(["uv", "run", "src/scripts/display_prof_edt.py", "--prof", "Marc Lang"])

if st.button("5. EDT Séraphine Grellier"):
    run_cmd(
        ["uv", "run", "src/scripts/display_prof_edt.py", "--prof", "Séraphine Grellier"]
    )


prof_nom = st.text_input("Insérer le nom du professeur :", "Marc Lang")

if st.button(f"Générer l'EDT pour {prof_nom}"):
    run_cmd(["uv", "run", "src/scripts/display_prof_edt.py", "--prof", prof_nom])
