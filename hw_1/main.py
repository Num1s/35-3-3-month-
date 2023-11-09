import asyncio
import logging
from os import getenv

from handlers.picture import picture_router
from handlers.start import start_router
from handlers.myinfo import myinfo_router

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

TOKEN = "6595789384:AAH9Yl6JCvCKw7FBNWqFlypZVJuPpc6CVro"

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # Register all the routers from handlers package
    dp.include_routers(
        start_router,
        picture_router,
        myinfo_router
    )

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())