import asyncio
import logging

from bot import bot, dp
from handlers import myinfo_router, picture_router, start_router, shop_router

async def main():
    dp.include_routers(
        start_router,
        myinfo_router,
        picture_router,
        shop_router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())