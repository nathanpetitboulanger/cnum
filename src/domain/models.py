from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Session:
    """
    Représente une session de cours unique dans l'emploi du temps.
    """

    course_name: str
    start_time: datetime
    end_time: datetime
    professors: List[str]
    course_type: Optional[str] = None
    room: Optional[str] = None
    group: Optional[str] = None
    color_rgb: Optional[str] = None

    def __post_init__(self):
        """
        Cette méthode s'exécute automatiquement après la création de l'objet.
        On s'assure que les dates sont bien des objets datetime.
        """
        # Conversion de start_time
        if isinstance(self.start_time, str):
            try:
                self.start_time = datetime.fromisoformat(self.start_time)
            except ValueError:
                self.start_time = datetime.strptime(
                    self.start_time, "%Y-%m-%d %H:%M:%S"
                )

        # Conversion de end_time
        if isinstance(self.end_time, str):
            try:
                self.end_time = datetime.fromisoformat(self.end_time)
            except ValueError:
                self.end_time = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")

    @property
    def duration_hours(self) -> float:
        """
        Calcule dynamiquement la durée du cours en heures.
        """
        if not isinstance(self.start_time, datetime) or not isinstance(
            self.end_time, datetime
        ):
            return 0.0
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600

    def has_professor(self, name: str) -> bool:
        """Vérifie si un professeur spécifique participe à cette session."""
        return any(name.lower() in p.lower() for p in self.professors)
