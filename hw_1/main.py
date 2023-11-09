import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import random
import os

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6595789384:AAH9Yl6JCvCKw7FBNWqFlypZVJuPpc6CVro")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(f"Hello! {message.from_user.first_name}")

@dp.message(Command("myinfo"))
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

@dp.message(Command("picture"))
async def cmd_picture(message: types.Message):
    image = random.choice(os.listdir(path='./images'))
    image = types.FSInputFile(f'./images/{image}')
    await message.reply_photo(caption=f'Success!', photo=image)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())