import pandas as pd
import ast
import sys
import os

# Ajout du chemin pour pouvoir importer nos modules
sys.path.append(os.getcwd())

from src.models.session import Session

def demo():
    print("--- Démonstration du passage à l'Objet ---")
    
    # 1. On charge les données brutes
    df = pd.read_csv('finale.csv').head(5)

    sessions = []

    for _, row in df.iterrows():
        # Conversion du texte "['Prof1', 'Prof2']" en liste Python []
        try:
            profs = ast.literal_eval(row['prof']) if isinstance(row['prof'], str) and row['prof'].startswith('[') else []
        except:
            profs = []
            
        # 2. On instancie (on crée) l'objet Session
        s = Session(
            course_name=row['cours'],
            start_time=row['start'],
            end_time=row['end'],
            professors=profs,
            course_type=row['type_cours'] if pd.notna(row['type_cours']) else None,
            group=row['groupe_etudiant'] if pd.notna(row['groupe_etudiant']) else None
        )
        sessions.append(s)

    # 3. On manipule des objets, pas des index de tableaux
    for s in sessions:
        print(f"\n[OBJET SESSION] : {s.course_name}")
        print(f"    Début    : {s.start_time}")
        print(f"    Durée    : {s.duration_hours}h")
        print(f"    Profs    : {', '.join(s.professors) if s.professors else 'Aucun'}")
        
        # Exemple d'utilisation d'une méthode de la classe
        if s.has_professor("Benjamin Pey"):
            print("    -> Alerte : M. Pey enseigne ici !")

if __name__ == "__main__":
    demo()
