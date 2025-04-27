# handlers/start.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu import main_menu

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Привет!\n\nЯ - твой личный помощник в бизнесе! "
        "Я помогу тебе не забыть о задачах, а также помогу своим ИИ для решения проблем.",
        reply_markup=main_menu()
    )