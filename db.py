import aiosqlite
from datetime import datetime

DB_NAME = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            join_date TEXT
        )
        """)
        await db.commit()

async def add_user(user_id: int, name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        now = datetime.now().strftime("%Y-%m-%d")
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, name, join_date) VALUES (?, ?, ?)",
            (user_id, name, now)
        )
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, join_date FROM users") as cursor:
            return await cursor.fetchall()
