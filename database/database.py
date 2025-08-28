import aiosqlite
from aiogram.types import Message
from aiosqlite import Cursor

from settings import settings


async def create_tables():
    async with aiosqlite.connect(settings.db.db_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                firstname TEXT,
                lastname TEXT,
                email TEXT
            )
        ''')

async def create_user(message: Message):
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (message.from_user.id,))
        user = await cursor.fetchone()
        if not user:
            await db.execute('''
            INSERT INTO users (user_id, firstname, lastname) VALUES (?, ?, ?)
            ''', (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await db.commit()
