from dataclasses import dataclass, field
from typing import List, Set
from .models import Session

@dataclass
class Timetable:
    """
    Conteneur pour un ensemble de sessions de cours.
    Permet d'effectuer des recherches et des statistiques globales.
    """
    sessions: List[Session] = field(default_factory=list)

    def add_session(self, session: Session):
        """Ajoute une session à l'emploi du temps."""
        self.sessions.append(session)

    @property
    def total_hours(self) -> float:
        """Calcule le total des heures de toutes les sessions présentes."""
        return sum(s.duration_hours for s in self.sessions)

    @property
    def teachers(self) -> Set[str]:
        """Renvoie la liste unique de tous les professeurs dans cet emploi du temps."""
        all_teachers = set()
        for s in self.sessions:
            all_teachers.update(s.professors)
        return all_teachers

    def filter_by_teacher(self, teacher_name: str) -> 'Timetable':
        """
        Renvoie un NOUVEL objet Timetable contenant uniquement 
        les cours d'un professeur donné.
        """
        filtered_sessions = [
            s for s in self.sessions 
            if s.has_professor(teacher_name)
        ]
        return Timetable(sessions=filtered_sessions)

    def __len__(self):
        """Permet d'utiliser len(timetable) pour avoir le nombre de sessions."""
        return len(self.sessions)
