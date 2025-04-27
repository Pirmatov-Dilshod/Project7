# handlers/reports.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import db
from utils.pdf_generator import generate_report
import aiosqlite
from config import ADMIN_IDS


router = Router()

@router.callback_query(F.data == "report")
async def report_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in ADMIN_IDS:
        await callback.message.answer("🚫 У вас нет доступа к отчетам.")
        await callback.answer()
        return

    pdf_path = await generate_report(user_id)
    await callback.message.answer_document(document=open(pdf_path, "rb"), caption="📄 Ваш отчет готов!")
    await callback.answer()