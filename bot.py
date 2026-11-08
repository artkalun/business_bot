import datetime
import logging
import os
import sys

import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from core.filters import OwnerCheck

load_dotenv('.env')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message):
    await message.answer('Hello World!')


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
