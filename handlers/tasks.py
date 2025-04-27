# handlers/tasks.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ForceReply
from database import db
import aiosqlite

router = Router()

@router.callback_query(F.data == "tasks")
async def tasks_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect(db.DB_NAME) as conn:
        cursor = await conn.execute("SELECT description FROM tasks WHERE user_id = ?", (user_id,))
        tasks = await cursor.fetchall()

    if tasks:
        tasks_text = "\n".join([f"🔹 {task[0]}" for task in tasks])
        await callback.message.answer(f"📋 Ваши задачи на сегодня:\n\n{tasks_text}")
    else:
        await callback.message.answer("📋 У вас пока нет задач на сегодня.")

    await callback.message.answer(
        "➕ Хотите добавить новую задачу? Просто отправьте её сюда:",
        reply_markup=ForceReply(selective=True)
    )
    await callback.answer()

@router.message(F.reply_to_message & F.reply_to_message.text.contains("добавить новую задачу"))
async def add_task_handler(message: Message):
    user_id = message.from_user.id
    task = message.text
    async with aiosqlite.connect(db.DB_NAME) as conn:
        await conn.execute(
            "INSERT INTO tasks (user_id, description, date) VALUES (?, ?, DATE('now'))",
            (user_id, task)
        )
        await conn.commit()
    await message.answer("✅ Задача успешно добавлена!")
