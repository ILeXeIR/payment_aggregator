import asyncio

from src.bot.deps import start_bot


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
