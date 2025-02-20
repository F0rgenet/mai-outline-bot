import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from src import generate_ics_file, get_schedule_entries

load_dotenv()

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN") or ""
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь название группы, и я пришлю тебе файл с расписанием.")

@dp.message()
async def schedule_handler(message: types.Message):
    group_name = message.text or ""
    if not group_name:
        await message.reply("Привет! Отправь название группы, и я пришлю тебе файл с расписанием.")
    await message.reply("Получаю расписание, пожалуйста, подождите...")
    try:
        entries = await get_schedule_entries(group_name)
        file_path = generate_ics_file(entries)
        await message.reply_document(document=FSInputFile(file_path),
                                     caption=f"Расписание для группы {group_name}")
    except Exception as e:
        await message.reply(f"Ошибка при получении расписания: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
