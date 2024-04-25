from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime
from pytz import timezone

import logging
import traceback
import asyncio
import os

from config import DEBUG, config

if not DEBUG:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


loop = asyncio.get_event_loop()
bot = Bot(config.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(loop=loop, storage=MemoryStorage())


TZ = timezone(config.tz)
ENGINE = create_async_engine(url=config.db_url)


def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        logging.warning(f'=====\n{now}\n{ex_traceback}\n{message}\n=====')
    else:
        logging.warning(f'=====\n{now}\n{message}\n=====')


async def set_up_menu() -> None:
    await bot.set_my_commands(
        [types.BotCommand(command="start", description="🔄 Обновить")]
    )
