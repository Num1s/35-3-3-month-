from aiogram import Router, types
from aiogram.filters.command import Command

myinfo_router = Router()

@myinfo_router.message(Command("myinfo"))
async def cmd_myinfo(message: types.Message):
    # print(
    await message.reply(f"""
    Ваши данные:
    ID: {message.from_user.id}
    Full Name: {message.from_user.full_name}
    First Name: {message.from_user.first_name}
    Last Name: {message.from_user.last_name}
    Username: {message.from_user.username}
    Telegram Premium: {'Отсутствует' if message.from_user.is_premium is None else 'Присутствует'}
    """)