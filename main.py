import logging
import sys
import asyncio

from handlers import dp
from init import log_error, bot, set_up_menu
from db.base import init_models
from config import DEBUG


async def main() -> None:
    await init_models()
    await set_up_menu()
    await dp.start_polling(bot)


if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig (level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', with_traceback=False)
    asyncio.run (main ())
