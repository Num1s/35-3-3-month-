import asyncio
import logging
from aiogram.types import BotCommand

from bot import bot, dp
from handlers import myinfo_router, picture_router, start_router, shop_router

async def main():
	await bot.set_my_commands([
		BotCommand(command="start", description="Начало"),
		BotCommand(command="picture", description="Показать картинку"),
		BotCommand(command="shop", description="Магазин"),
		BotCommand(command="myinfo", description="Информация профиля"),
	])
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