# utils/notifier.py

import asyncio
from aiogram import Bot
from database import db
import aiosqlite
import datetime

async def morning_reminder(bot: Bot):
    while True:
        now = datetime.datetime.now()
        # Ждем до 09:00
        target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += datetime.timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()

        await asyncio.sleep(wait_seconds)

        # Отправляем напоминания всем пользователям
        async with aiosqlite.connect(db.DB_NAME) as conn:
            cursor = await conn.execute("SELECT DISTINCT user_id FROM users")
            users = await cursor.fetchall()

        for (user_id,) in users:
            try:
                await bot.send_message(
                    user_id,
                    "🌞 Доброе утро! Не забудьте поставить задачи на сегодня!"
                )
            except Exception:
                pass  # Игнорируем ошибки типа "пользователь заблокировал бота"
