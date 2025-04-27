# handlers/wishes.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ForceReply
from database import db
import aiosqlite

router = Router()

@router.callback_query(F.data == "wish")
async def wish_handler(callback: CallbackQuery):
    await callback.message.answer(
        "💬 Введите ваше пожелание для развития компании:",
        reply_markup=ForceReply(selective=True)
    )
    await callback.answer()

@router.message(F.reply_to_message & F.reply_to_message.text.contains("пожелание"))
async def add_wish_handler(message: Message):
    user_id = message.from_user.id
    wish = message.text
    async with aiosqlite.connect(db.DB_NAME) as conn:
        await conn.execute(
            "INSERT INTO wishes (user_id, wish, date) VALUES (?, ?, DATE('now'))",
            (user_id, wish)
        )
        await conn.commit()
    await message.answer("✅ Ваше пожелание успешно сохранено! Спасибо!")
