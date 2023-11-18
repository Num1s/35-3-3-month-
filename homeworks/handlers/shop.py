from aiogram import Router, types, F
from aiogram.filters.command import Command
from handlers.start import cmd_start
from db_utils.db_settings import Database
import asyncio
import json

shop_router = Router()
db = Database()

pages = []
page = 0 + 1


@shop_router.message(Command('shop'))
async def shop(message: types.Message):
	shop_keyboard = types.ReplyKeyboardMarkup(
		keyboard=[
			[
				types.KeyboardButton(
					text='Книги'
				),
				types.KeyboardButton(
					text='Soon...'
				),
				types.KeyboardButton(
					text='Soon...'
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

@shop_router.message(F.text == 'Книги')
async def cmd_item_1(message: types.Message):
	r = types.ReplyKeyboardRemove()
	data = await db.get_table()
	global pages, page
	pages = []
	page = 0
	loop_count = 0
	text = ''
	for i in data:
		status = 'В наличии' if i[4] == 1 else 'Не в наличии'
		loop_count += 1
		text += f'Книга №{i[0]} \n \nНазвание: {i[1]}\nЦена: {i[2]}\nАвтор: {i[3]}\nСтатус: {status}\n \n'
		if loop_count % 2 == 0 or loop_count - 1 == len(data) - 1:
			pages.append(text)
			text = ''
	await message.answer(f'Секунду, запрос обрабатывается...', reply_markup=r)
	await asyncio.sleep(10)
	pagination_keyboard = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				types.InlineKeyboardButton(
					text='◀️',
					callback_data='back_page'
				),
				types.InlineKeyboardButton(
					text=f'{page + 1}',
					callback_data='page'
				),
				types.InlineKeyboardButton(
					text='▶️',
					callback_data='next_page'
				)
			]
		]
	)
	await message.answer(pages[0], reply_markup=pagination_keyboard)


@shop_router.callback_query(F.data == 'back_page')
async def back_page_button(callback: types.CallbackQuery):
	global pages, page
	if page == 0:
		await callback.answer('Вы на самой начальной странице')
	else:
		page -= 1
	pagination_keyboard = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				types.InlineKeyboardButton(
					text='◀️',
					callback_data='back_page'
				),
				types.InlineKeyboardButton(
					text=f'{page + 1}',
					callback_data='page'
				),
				types.InlineKeyboardButton(
					text='▶️',
					callback_data='next_page'
				)
			]
		]
	)
	await callback.message.edit_text(pages[page], reply_markup=pagination_keyboard)

@shop_router.callback_query(F.data == 'next_page')
async def next_page_button(callback: types.CallbackQuery):
	global pages, page
	if page == len(pages) - 1:
		await callback.answer('Вы дошли до конца страницы')
	else:
		page += 1
	pagination_keyboard = types.InlineKeyboardMarkup(
		inline_keyboard=[
			[
				types.InlineKeyboardButton(
					text='◀️',
					callback_data='back_page'
				),
				types.InlineKeyboardButton(
					text=f'{page + 1}',
					callback_data='page'
				),
				types.InlineKeyboardButton(
					text='▶️',
					callback_data='next_page'
				)
			]
		]
	)
	await callback.message.edit_text(pages[page], reply_markup=pagination_keyboard)

@shop_router.callback_query(F.data == 'page')
async def next_page_button(callback: types.CallbackQuery):
	global page
	await callback.answer(f'Вы на странице - {page + 1}')

@shop_router.callback_query(F.data == 'start')
async def cmd_item_4(callback: types.CallbackQuery):
	r = types.ReplyKeyboardRemove()
	await callback.answer('Успешно!')
	await cmd_start(callback=callback)
	await callback.message.answer(f'Вы успешно вернулись в начало', reply_markup=r)


