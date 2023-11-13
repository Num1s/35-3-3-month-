from aiogram import Router, F, types
from aiogram.filters.command import Command

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    start_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='Контакты',
                    url="https://instagram.com"
                ),
                types.InlineKeyboardButton(
                    text='Адрес',
                    url='https://youtube.com'
                ),
                types.InlineKeyboardButton(
                    text='О нас',
                    url='https://nike.com'
                )
            ]
        ]
    )
    await message.reply(f"Hello! {message.from_user.first_name}", reply_markup=start_keyboard)