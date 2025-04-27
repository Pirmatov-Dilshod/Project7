# keyboards/menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 О нас", callback_data="about")],
        [InlineKeyboardButton(text="🤖 Помощь от ИИ", callback_data="ai_help")],
        [InlineKeyboardButton(text="📋 Задачи на сегодня", callback_data="tasks")],
        [InlineKeyboardButton(text="✅ Отметиться", callback_data="checkin")],
        [InlineKeyboardButton(text="💡 Внести пожелание", callback_data="wish")],
        [InlineKeyboardButton(text="📄 Отправить отчет", callback_data="report")],
        [InlineKeyboardButton(text="📈 Статистика за неделю", callback_data="stats")],
    ])
    return keyboard
