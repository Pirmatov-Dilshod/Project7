# handlers/checkin.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import db
import aiosqlite

router = Router()

@router.callback_query(F.data == "checkin")
async def checkin_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect(db.DB_NAME) as conn:
        await conn.execute(
            "INSERT INTO checkins (user_id, date) VALUES (?, DATE('now'))",
            (user_id,)
        )
        await conn.commit()

    await callback.message.answer("✅ Вы успешно отметились сегодня! Отличная работа 💪")
    await callback.answer()
