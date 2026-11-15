import datetime
import logging
import os
import sqlite3
import sys

import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from core.filters import OwnerCheck

load_dotenv('.env')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dp = Dispatcher()

conn = sqlite3.connect('database.db')
cur = conn.cursor()


@dp.message(CommandStart())
async def start(message):
    await message.answer('Hello World!')


@dp.business_message(OwnerCheck(), F.text)
async def text_handler(message):
    cur.execute(
        "INSERT INTO messages (id, sent_at, type, content) VALUES (?, ?, \"text\", ?)",
        (message.message_id, message.date.isoformat(), message.text)
    )

    conn.commit()


@dp.business_message(OwnerCheck(), F.photo)
async def photo_handler(message, bot):
    file_id = max(message.photo, key=lambda x: x.file_size).file_id
    file = (await bot.get_file(file_id)).file_path
    await bot.download_file(file, f'storage\\{message.message_id}{os.path.splitext(file)[1]}')

    if message.caption:
        cur.execute(
            "INSERT INTO messages (id, sent_at, type, conetnt, file_expired) VALUES (?, ?, \"photo\", ?, 0)",
            (message.message_id, message.date.isoformat(), message.caption)
        )
    else:
        cur.execute(
            "INSERT INTO messages (id, sent_at, type, file_expired) VALUES (?, ?, \"photo\", 0)",
            (message.message_id, message.date.isoformat())
        )

    conn.commit()
        


async def main():
    bot = Bot(token=os.getenv('BOT-TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


def logging_debug():
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(name)s: %(message)s')
    console_formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')  

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('logs\\last_log.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    start_time = datetime.datetime.now()

    file_handler2 = logging.FileHandler(f'logs\\{start_time.strftime("%y-%m-%d %H.%M.%S")}.log', mode='w')
    file_handler2.setLevel(logging.DEBUG)
    file_handler2.setFormatter(file_formatter)
    logger.addHandler(file_handler2)


if __name__ == "__main__":
    logging_debug()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
