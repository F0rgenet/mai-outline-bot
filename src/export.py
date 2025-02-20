from pathlib import Path

from typing import List
from icalendar import Calendar, Event
from collections import defaultdict
from loguru import logger

from .model import Entry

ICS_DOW_MAP = {0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA", 6: "SU"}

TYPE_COLORS = {
    "ЛК": "#FF8888",
    "ПЗ": "#88FF88",
    "ЛР": "#8888FF",
    "ЭК": "#FFD700",
}

def generate_ics_file(entries: List["Entry"], filename: str = "schedule.ics") -> Path:
    cal = Calendar()
    cal.add("prodid", "-//MAI Schedule//RU")
    cal.add("version", "2.0")

    groups = defaultdict(list)
    for entry in entries:
        key = (entry.name, entry.type)
        logger.debug(key)
        groups[key].append(entry)

    logger.debug(len(groups))

    for key, group_entries in groups.items():
        base_entry = group_entries[0]
        event = Event()
        event.add("summary", f"{base_entry.name} ({base_entry.type})")

        if base_entry.lector:
            desc = f"Лектор: {base_entry.lector}"
        event.add("description", desc)

        if base_entry.room:
            event.add("location", base_entry.room)

        event.add("dtstart", base_entry.start)
        event.add("dtend", base_entry.end)

        rdate_values = [e.start for e in group_entries if e.start != base_entry.start]
        if rdate_values:
            event.add("RDATE", rdate_values)

        if base_entry.type in TYPE_COLORS:
            event.add("X-COLOR", TYPE_COLORS[base_entry.type])

        cal.add_component(event)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())
        return Path(filename)
