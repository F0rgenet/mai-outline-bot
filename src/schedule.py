import hashlib
import locale
from datetime import datetime

import aiohttp
from loguru import logger
from fake_useragent import UserAgent

from .model import Entry

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def get_group_hash(group: str) -> str:
    return hashlib.md5(group.encode('utf-8')).hexdigest()

def get_group_url(group: str) -> str:
    url = "https://public.mai.ru/schedule/data/{}.json"
    result = url.format(get_group_hash(group))
    logger.info(f"Получена ссылка на группу {group}: {result}")
    return result

async def get_group_data(group: str) -> dict:
    async with aiohttp.ClientSession(
        headers={"User-Agent": UserAgent().chrome},
        cookies={"schedule-group-cache": "2.0"},
        raise_for_status=True
    ) as session:
        async with session.get(get_group_url(group)) as response:
            result: dict = await response.json()
            result.pop("group", None)
            return result

def fetch_entry(name: str, data: dict, date: str) -> Entry:
    # Получаем данные лектора
    lector_dict = data.get("lector")
    lector = list(lector_dict.values())[0] if lector_dict else None
    if lector == "" or lector is None:
        lector = None

    # Получаем данные аудитории
    room_dict = data.get("room")
    room = list(room_dict.values())[0] if room_dict else None
    if room is None or "--каф" in room:
        room = None

    entry_type = list(data["type"].keys())[0]
    start = datetime.strptime(f"{date} {data['time_start']}", "%d.%m.%Y %H:%M:%S")
    end = datetime.strptime(f"{date} {data['time_end']}", "%d.%m.%Y %H:%M:%S")
    
    return Entry(
        name=name,
        start=start,
        end=end,
        type=entry_type,
        lector=lector,
        room=room
    )

def fetch_day(day_data: dict, date: str) -> list:
    result = []
    pairs = day_data.get("pairs", {})
    for pair in pairs.values():
        for name, subdata in pair.items():
            entry = fetch_entry(name, subdata.copy(), date)
            result.append(entry)
    return result

async def get_schedule_entries(group: str) -> list:
    data = await get_group_data(group)
    entries = []
    for date, day_data in data.items():
        entries.extend(fetch_day(day_data, date))
    return entries
