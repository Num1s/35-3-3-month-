from aiogram import Router, F, types
from aiogram.filters import Command
from db_utils.db_settings import Database

admin_router = Router()
db = Database()

BAD_WORDS = ['плохой', 'дурак', 'тупой', 'придурок', 'даун', 'додик'
             'бля', 'сука', 'ебало', 'заебал', 'блять', 'трахал', 'членожуй',
             'членосос', 'спермоглот', 'хуеглот', 'хуесос', 'чё', 'че', 'сковорода', 'пизда',
             'привет', 'лох', 'да', 'нет', 'спс'
             ]

@admin_router.message(F.chat.type == "supergroup")
async def catch_bad_words(message: types.Message):
    user = message.from_user
    await db.insert_user(user)
    for i in BAD_WORDS:
        if i in message.text.lower():
            await db.insert_user_warn(message.from_user, i)
            data = await db.get_user_warn(message.from_user, 'one') if \
                await db.get_user_warn(message.from_user, 'one') else 0
            await message.reply(f'Вы были предупреждены за использование ненормативной лексики | {data[0]}/3! ({message.chat.id})')
            break

@admin_router.message(Command("almat"))
async def almat_test(message: types.Message):
    await message.reply(f'almat test')