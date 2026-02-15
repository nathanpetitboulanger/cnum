import pandas as pd
import ast
import sys
import os

sys.path.append(os.getcwd())

from src.models.session import Session
from src.models.timetable import Timetable

def demo_oop():
    print("--- Démonstration de la hiérarchie d'Objets ---")
    
    # 1. Chargement et création des objets Session
    df = pd.read_csv('finale.csv')
    
    # On crée notre objet principal
    my_timetable = Timetable()

    for _, row in df.iterrows():
        try:
            profs = ast.literal_eval(row['prof']) if isinstance(row['prof'], str) and row['prof'].startswith('[') else []
        except:
            profs = []
            
        s = Session(
            course_name=row['cours'],
            start_time=row['start'],
            end_time=row['end'],
            professors=profs,
            course_type=row['type_cours'] if pd.notna(row['type_cours']) else None
        )
        # On ajoute la session dans notre "boîte" Timetable
        my_timetable.add_session(s)

    # 2. Utilisation des méthodes de Timetable
    print(f"Nombre total de sessions : {len(my_timetable)}")
    print(f"Total d'heures global     : {my_timetable.total_hours:.2f}h")
    
    # 3. Filtrage intelligent
    target_prof = "Benjamin Pey"
    prof_timetable = my_timetable.filter_by_teacher(target_prof)
    
    print(f"\nStats pour {target_prof} :")
    print(f"  - Nombre de cours : {len(prof_timetable)}")
    print(f"  - Volume horaire  : {prof_timetable.total_hours:.2f}h")
    
    # 4. Découvrir tous les profs
    print("\nListe des profs détectés (5 premiers) :")
    # On trie pour avoir un résultat stable
    sorted_teachers = sorted(list(my_timetable.teachers))
    print(sorted_teachers[:5])

if __name__ == "__main__":
    demo_oop()
