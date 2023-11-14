from aiogram import Router, F, types
from aiogram.filters.command import Command
import aiogram

start_router = Router()

@start_router.message(Command('start'))
async def cmd_start(message: types.Message = None, callback: types.CallbackQuery = None):
    start_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='Контакты',
                    callback_data='contacts'
                ),
                types.InlineKeyboardButton(
                    text='Адрес',
                    callback_data='adress'
                ),
                types.InlineKeyboardButton(
                    text='О нас',
                    callback_data='about'
                )
            ],
            [
                types.InlineKeyboardButton(
                    text='Перейти в магазин',
                    callback_data='shop'
                ),
                types.InlineKeyboardButton(
                    text='Наш сайт',
                    url='https://google.com'
                )
            ]
        ]
    )
    if callback and message is None:
        message = callback.message
        user = callback.from_user.first_name
    else:
        user = message.from_user.first_name

    await message.answer(f"Hello! {user} | Выберите опцию в нижней категории!", reply_markup=start_keyboard)

@start_router.callback_query(F.data == 'contacts')
async def contacts_callback(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await callback.message.answer('Наши контакты: ...')

@start_router.callback_query(F.data == 'adress')
async def adress_callback(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await callback.message.answer('Наш адрес: ...')

@start_router.callback_query(F.data == 'about')
async def about_callback(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await callback.message.answer('О нас: ...')

@start_router.callback_query(F.data == 'shop')
async def about_callback(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await callback.message.answer('/shop -> нажмите на команду, для того чтобы открыть меню с товарами')