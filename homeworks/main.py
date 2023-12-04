import asyncio
import logging
from datetime import datetime
from aiogram import *
from aiogram.types import BotCommand

from bot import bot, dp, scheduler
from db_utils.db_settings import Database
from handlers import myinfo_router, picture_router, start_router, shop_router, fsmadmin_router, admin_router


async def db_settings():
	db = Database()
	await db.create_table()

async def scheduler_default(chat_id, text):
	await bot.send_message(chat_id, text=text)

async def scheduler_settings():
	db = Database()
	for i in await db.get_users_scheduler():
		scheduler.add_job(
			scheduler_default,
			"date",
			run_date=datetime.strptime(i[2], '%d-%m-%Y %H:%M'),
			kwargs={"chat_id": i[0], "text": i[1]}
		)


async def scheduler_admin():
	db = Database()
	users = await db.get_users()
	for i in users:
		item = await db.get_user_warn(await bot.get_chat(i[0]), 'one')
		if item:
			if item[0] >= 3:
				user = await bot.get_chat(item[1])
				await bot.send_message(text=f'{user.username} был забанен по причине: Многократное использование ненормативной лексики', chat_id=-1002014053456)
				await bot.ban_chat_member(chat_id=-1002014053456, user_id=user.id)
				await db.delete_user_warn(user)


async def on_startup():
	scheduler.add_job(
		scheduler_settings,
		"interval",
		seconds=40
	)
	scheduler.add_job(
		scheduler_admin,
		"interval",
		seconds=10
	)


async def main():
	await bot.set_my_commands([
		BotCommand(command="start", description="Начало"),
		BotCommand(command="picture", description="Показать картинку"),
		BotCommand(command="shop", description="Магазин"),
		BotCommand(command="myinfo", description="Информация профиля"),
		BotCommand(command="quest", description="Пройти опрос"),
	])
	dp.startup.register(db_settings)
	dp.startup.register(on_startup)
	dp.include_routers(
		myinfo_router,
		picture_router,
		shop_router,
		fsmadmin_router,
		admin_router,
		start_router
	)
	scheduler.start()
	await dp.start_polling(bot)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())