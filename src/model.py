from typing import Literal, Optional
from datetime import datetime

class Entry:
    def __init__(self, name: str, start: datetime, end: datetime, type: Literal["ЛК", "ПЗ", "ЛР", "ЭК"], 
                 lector: Optional[str]=None, room: Optional[str] = None):
        self.name = name
        self.start = start
        self.end = end
        self.lector = lector
        self.type = type
        self.room = room

    def __repr__(self):
        return f"Пара({self.name}, ведёт: {self.lector}, время: {self.start}-{self.end}, тип: {self.type}, помещение: {self.room})"