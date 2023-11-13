from aiogram import Router, types, F
from aiogram.filters.command import Command
from handlers.start import cmd_start

shop_router = Router()

@shop_router.message(Command('shop'))
async def shop(message: types.Message):
    shop_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text='Удочка'
                ),
                types.KeyboardButton(
                    text='Древесина'
                ),
                types.KeyboardButton(
                    text='Алмаз'
                ),
                types.KeyboardButton(
                    text='В начало'
                )
            ]
        ]
    )
    await message.answer(f'Выберите товар, в меню кнопок ниже...', reply_markup=shop_keyboard)

@shop_router.message(F.text == 'Удочка')
async def cmd_item_1(message: types.Message):
    r = types.ReplyKeyboardRemove()
    await message.answer(f'Вы купили удочку.', reply_markup=r)

@shop_router.message(F.text == 'Древесина')
async def cmd_item_2(message: types.Message):
    r = types.ReplyKeyboardRemove()
    await message.answer(f'Вы купили древесину.', reply_markup=r)

@shop_router.message(F.text == 'Алмаз')
async def cmd_item_3(message: types.Message):
    r = types.ReplyKeyboardRemove()
    await message.answer(f'Вы купили алмаз.', reply_markup=r)

@shop_router.message(F.text == 'В начало')
async def cmd_item_4(message: types.Message):
    r = types.ReplyKeyboardRemove()
    await message.answer(f'Вы успешно вернулись в начало', reply_markup=r)
    await cmd_start(message)
