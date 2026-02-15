from typing import Protocol
from src.domain.timetable import Timetable

class TimetableRepository(Protocol):
    def load(self) -> Timetable:
        ...

class TimetableRenderer(Protocol):
    def render(self, timetable: Timetable):
        ...
