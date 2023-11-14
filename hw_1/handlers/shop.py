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
				)
			]
		],
	)
	return_keyboard = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				types.InlineKeyboardButton(
					text='В начало',
					callback_data='start'
				)
			]
		]
	)
	await message.reply('Категории...', reply_markup=shop_keyboard)
	await message.answer(f'Для того чтобы выйти в начало, нажмите на кнопку ниже', reply_markup=return_keyboard)

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

@shop_router.callback_query(F.data == 'start')
async def cmd_item_4(callback: types.CallbackQuery):
	r = types.ReplyKeyboardRemove()
	await callback.answer('Успешно!')
	await cmd_start(callback=callback)
	await callback.message.answer(f'Вы успешно вернулись в начало', reply_markup=r)


