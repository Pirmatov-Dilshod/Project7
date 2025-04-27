# bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from database.db import init_db
from utils.cleaner import delete_old_tasks
from utils.notifier import morning_reminder
from handlers import start, about, tasks, checkin, wishes, reports

async def main():
    # Настройка логирования в консоль и файл
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    # Инициализация бота с правильными параметрами
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Инициализация базы данных
    await init_db()

    # Регистрация всех роутеров
    dp.include_router(start.router)
    dp.include_router(about.router)
    dp.include_router(tasks.router)
    dp.include_router(checkin.router)
    dp.include_router(wishes.router)
    dp.include_router(reports.router)

    # Удаляем старые апдейты
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск фоновых задач
    asyncio.create_task(periodic_clean())
    asyncio.create_task(morning_reminder(bot))

    # Запуск polling
    logging.info("Бот успешно запущен. Ожидание обновлений...")
    await dp.start_polling(bot)

async def periodic_clean():
    """Фоновая задача для ежедневной очистки старых данных."""
    while True:
        await delete_old_tasks()
        await asyncio.sleep(86400)  # Пауза 24 часа

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен вручную.")
