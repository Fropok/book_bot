from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_MENU_RU


async def set_main_menu(bot: Bot) -> None:
    commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_MENU_RU['main'].items()
    ]

    await bot.set_my_commands(commands)
