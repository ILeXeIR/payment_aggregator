import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.settings import settings
from .handlers import handlers_router


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TG_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(handlers_router)

commands = [
    BotCommand(
        command="start",
        description="Bot description"
    ),
    BotCommand(
        command="help",
        description="Help"
    ),
    BotCommand(
        command="check",
        description="Check connection to DB"
    )
]


async def start_bot():
    try:
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

