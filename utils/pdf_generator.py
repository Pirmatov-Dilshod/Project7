# utils/pdf_generator.py
from fpdf import FPDF

from database import db
import aiosqlite

async def generate_report(user_id: int) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Отчет по задачам и пожеланиям", ln=True, align="C")
    pdf.ln(10)

    async with aiosqlite.connect(db.DB_NAME) as conn:
        # Задачи
        pdf.cell(200, 10, txt="📋 Задачи:", ln=True)
        cursor = await conn.execute("SELECT description FROM tasks WHERE user_id = ?", (user_id,))
        tasks = await cursor.fetchall()
        if tasks:
            for task in tasks:
                pdf.cell(200, 10, txt=f"🔹 {task[0]}", ln=True)
        else:
            pdf.cell(200, 10, txt="Нет задач.", ln=True)

        pdf.ln(10)

        # Пожелания
        pdf.cell(200, 10, txt="💬 Пожелания:", ln=True)
        cursor = await conn.execute("SELECT wish FROM wishes WHERE user_id = ?", (user_id,))
        wishes = await cursor.fetchall()
        if wishes:
            for wish in wishes:
                pdf.cell(200, 10, txt=f"🔸 {wish[0]}", ln=True)
        else:
            pdf.cell(200, 10, txt="Нет пожеланий.", ln=True)

    # Сохраняем
    file_path = f"user_{user_id}_report.pdf"
    pdf.output(file_path)

    return file_path
