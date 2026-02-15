import sys
import os

sys.path.append(os.getcwd())

from src.core.parser import CSVTimetableParser
from src.io.ical_exporter import ICalExporter

def main():
    print("=== CNUM - Logiciel d'Emploi du Temps (Full POO) ===")
    
    # 1. On charge l'emploi du temps complet
    parser = CSVTimetableParser()
    full_timetable = parser.parse('finale.csv')
    print(f"\n[1] Chargement OK : {len(full_timetable)} cours trouves.")

    # 2. On filtre pour un professeur spécifique (ex: Marc Lang)
    prof_nom = "Marc Lang"
    prof_timetable = full_timetable.filter_by_teacher(prof_nom)
    print(f"[2] Filtrage pour {prof_nom} : {len(prof_timetable)} cours.")

    # 3. On exporte le resultat en .ics
    if len(prof_timetable) > 0:
        exporter = ICalExporter(calendar_name=f"EDT de {prof_nom}")
        output_file = f"edt_{prof_nom.replace(' ', '_').lower()}.ics"
        
        exporter.export(prof_timetable, output_file)
        
        # Petit bonus : on affiche le total d'heures
        print(f"[3] Volume total pour ce prof : {prof_timetable.total_hours:.1f}h")
    else:
        print("[!] Aucun cours a exporter.")

if __name__ == "__main__":
    main()
