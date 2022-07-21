import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Text
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    count = db.count_users()[0]
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
        msg = f"{message.from_user.get_mention(as_html=True)} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    except sqlite3.IntegrityError as err:
        pass

    await message.answer("Xush kelibsiz!")
    # Adminga xabar beramiz
        
@dp.message_handler(Text(contains="#message", ignore_case=True), user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()   
    for user in users:
        try:    
            user_id = user[0]
            await bot.send_message(chat_id=user_id, text=message.text)
            await asyncio.sleep(0.05)
        except:
            pass     