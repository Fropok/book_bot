import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import load_config
from database.connection import MyDatabase
from keyboards.set_menu import set_main_menu
from handlers import commands_handlers, callback_handlers, other_handlers


async def start_bot() -> None:
    config = load_config()

    logging.basicConfig(
        level=config.logger.level,
        format=config.logger.format,
        encoding=config.logger.encoding,
    )

    db = MyDatabase(config.database.path, config.database.book_path)

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp['db'] = db

    dp.include_router(commands_handlers.router)
    dp.include_router(callback_handlers.router)
    dp.include_router(other_handlers.router)

    await set_main_menu(bot)

    await dp.start_polling(bot)


asyncio.run(start_bot())
