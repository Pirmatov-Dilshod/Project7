# handlers/about.py

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.answer(
        "🔷 Наша компания помогает бизнесам расти быстрее, благодаря автоматизации задач и внедрению ИИ-решений!\n\n"
        "✅ Работаем с 2010 года\n"
        "✅ Более 500 довольных клиентов\n"
        "✅ Профессиональная команда\n\n"
        "Спасибо, что с нами! 🚀"
    )
    await callback.answer()
