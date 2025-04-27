# handlers/stats.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import db
import aiosqlite

router = Router()

@router.callback_query(F.data == "stats")
async def stats_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect(db.DB_NAME) as conn:
        # Количество задач за последние 7 дней
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date >= DATE('now', '-7 days')",
            (user_id,)
        )
        tasks_count = (await cursor.fetchone())[0]

        # Количество пожеланий
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM wishes WHERE user_id = ? AND date >= DATE('now', '-7 days')",
            (user_id,)
        )
        wishes_count = (await cursor.fetchone())[0]

        # Количество отметок
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM checkins WHERE user_id = ? AND date >= DATE('now', '-7 days')",
            (user_id,)
        )
        checkins_count = (await cursor.fetchone())[0]

    text = (
        f"📈 <b>Ваша активность за 7 дней:</b>\n\n"
        f"✅ Задач добавлено: <b>{tasks_count}</b>\n"
        f"💬 Пожеланий отправлено: <b>{wishes_count}</b>\n"
        f"📅 Отметок: <b>{checkins_count}</b>"
    )

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
