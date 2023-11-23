import asyncio
import logging
from aiogram.types import BotCommand

from bot import bot, dp
from db_utils.db_settings import Database
from handlers import myinfo_router, picture_router, start_router, shop_router, fsmadmin_router

async def db_settings():
	db = Database()
	await db.create_table()
	await db.insert_default_category()
	await db.insert_default_book()

async def main():
	await bot.set_my_commands([
		BotCommand(command="start", description="Начало"),
		BotCommand(command="picture", description="Показать картинку"),
		BotCommand(command="shop", description="Магазин"),
		BotCommand(command="myinfo", description="Информация профиля"),
		BotCommand(command="quest", description="Пройти опрос"),
	])
	dp.startup.register(db_settings)
	dp.include_routers(
		start_router,
		myinfo_router,
		picture_router,
		shop_router,
		fsmadmin_router
	)
	await dp.start_polling(bot)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())