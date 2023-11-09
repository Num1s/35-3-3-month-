from aiogram import Router, types
from aiogram.filters import Command

import os
import random

picture_router = Router()

@picture_router.message(Command("picture"))
async def picture_handler(message: types.Message) -> None:
    image = random.choice(os.listdir(path='./images'))
    image = types.FSInputFile(f'./images/{image}')
    await message.reply_photo(caption=f'Success!', photo=image)