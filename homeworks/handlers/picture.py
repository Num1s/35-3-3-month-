from aiogram import Router, types
from aiogram.filters.command import Command
import random, os

picture_router = Router()

@picture_router.message(Command("picture"))
async def cmd_picture(message: types.Message):
    image = random.choice(
        os.listdir(
            path='./images'
        )
    )
    image = types.FSInputFile(f'./images/{image}')
    await message.reply_photo(caption=f'Success!', photo=image)