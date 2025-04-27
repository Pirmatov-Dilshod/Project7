# utils/cleaner.py

import aiosqlite
from database import db

async def delete_old_tasks():
    async with aiosqlite.connect(db.DB_NAME) as conn:
        await conn.execute("DELETE FROM tasks WHERE date < DATE('now', '-7 days')")
        await conn.commit()
