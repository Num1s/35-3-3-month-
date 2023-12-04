from aiogram import Router, F, types
from aiogram.filters.command import Command
from bot import scheduler
from db_utils.db_settings import Database
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

start_router = Router()
db = Database()

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
            ],
            [
                types.InlineKeyboardButton(
                    text='Подписаться на рассылку',
                    callback_data='scheduler_callback'
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


class AddScheduler(StatesGroup):
    text = State()
    date = State()

@start_router.callback_query(F.text == 'exit')
async def exit_callback(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы успешно вышли с опроса.')

@start_router.callback_query(F.data == 'scheduler_callback')
async def scheduler_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Для выхода введите слово - exit.')
    await state.set_state(AddScheduler.text)
    await callback.message.answer('Введите текст, который вы хотели-бы видеть через некоторое время.')

@start_router.message(F.text, AddScheduler.text)
async def text_callback(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AddScheduler.date)
    await message.answer('Введите дату, через которое вы хотели-бы видеть текст \nкоторый вы ввели ранее (Пример: 28-11-2023 15:00)')

@start_router.message(F.text, AddScheduler.date)
async def date_callback(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    try:
        time_data = datetime.strptime(data['date'], '%d-%m-%Y %H:%M')
        await db.insert_user_scheduler(message.from_user.id, data['text'], data['date'])
        await message.answer('Готово!')
    except ValueError:
        await message.answer('Дата была введена неверно, просим пройти опрос заново')

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