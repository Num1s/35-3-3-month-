from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

fsmadmin_router = Router()


class Quotes(StatesGroup):
    name = State()
    age = State()
    gender = State()
    exp = State()
    route = State()
    exp_who = State()

@fsmadmin_router.message(Command("stop"), F.text == "stop")
async def stop_quotes(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы прервали опрос.")

@fsmadmin_router.message(Command("quest"))
async def start_quotes(message: types.Message, state: FSMContext):
    await message.answer("Для выхода введите 'stop'")
    await state.set_state(Quotes.name)
    await message.answer("Введите ваше имя.")

@fsmadmin_router.message(F.text, Quotes.name)
async def name_quotes(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Quotes.age)
    await message.answer("Введите ваш возвраст.")

@fsmadmin_router.message(F.text, Quotes.age)
async def name_quotes(message: types.Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit():
        await message.answer("Возраст должен быть числом")
    elif int(age) < 12 or int(age) > 100:
        await message.answer("Возраст должен быть от 12 до 100")
    else:
        await state.update_data(age=int(age))
        await state.set_state(Quotes.gender)
        await message.answer("Введите ваш пол.")

@fsmadmin_router.message(F.text, Quotes.gender)
async def name_quotes(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Quotes.exp)
    await message.answer("Ваш стаж в программировании? (Пример: 5 лет)")

@fsmadmin_router.message(F.text, Quotes.exp)
async def name_quotes(message: types.Message, state: FSMContext):
    await state.update_data(exp=message.text)
    await state.set_state(Quotes.route)
    await message.answer("Введите ваше направление в программировании. (Пример: Backend, Frontend, Android, Ios)")

@fsmadmin_router.message(F.text, Quotes.route)
async def name_quotes(message: types.Message, state: FSMContext):
    await state.update_data(route=message.text)
    await state.set_state(Quotes.exp_who)
    await message.answer("Введите ваш уровень в программировании. (Пример: Junior, Middle, Senior)")

@fsmadmin_router.message(F.text, Quotes.exp_who)
async def name_quotes(message: types.Message, state: FSMContext):
    exp = message.text.strip()
    if exp.lower() not in ['junior', 'middle', 'senior']:
        await message.answer('Вы указали неверный уровень. Пример: (junior, middle, senior)')
    else:
        await state.update_data(exp_who=message.text)
        data = await state.get_data()
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Да',
                        callback_data='yes'
                    ),
                    types.InlineKeyboardButton(
                        text='Нет',
                        callback_data='no'
                    )
                ]
            ]
        )
        await message.answer(f"""
        Вывод:
        
        Имя: {data['name']}
        Возвраст: {data['age']}
        Пол: {data['gender']}
        Стаж: {data['exp']}
        Направление: {data['route']}
        Уровень в программировании: {data['exp_who']}

        Потвердите действие, чтобы отправить форму...
        """, reply_markup=kb)

@fsmadmin_router.callback_query(F.data == 'yes')
async def button_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Успешно!')
    data = await state.get_data()
    with open('msg.txt', 'w', encoding='utf-8') as f:
        description = f'''
        Пользователь: {callback.from_user.first_name}
        
        Имя: {data['name']}
        Возвраст: {data['age']}
        Пол: {data['gender']}
        Стаж: {data['exp']}
        Направление: {data['route']}
        Уровень в программировании: {data['exp_who']}
        '''
        f.write(description)
    await callback.message.answer('Данные были сохранены.')
    await state.clear()

@fsmadmin_router.callback_query(F.data == 'no')
async def button_callback(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await stop_quotes()