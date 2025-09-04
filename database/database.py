import asyncio

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
                email TEXT,
                is_active INTEGER DEFAULT 0,
                msg_recieved INTEGER DEFAULT 0,
                is_privileged INTEGER DEFAULT 0
            )
        ''')


async def create_user(message: Message):
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (message.from_user.id,))
        user = await cursor.fetchone()
        if not user:
            if message.from_user.id == settings.bots.admin_id:
                await db.execute('''
                            INSERT INTO users (user_id, firstname, lastname, is_privileged) VALUES (?, ?, ?, ?)
                            ''', (message.from_user.id, message.from_user.first_name, message.from_user.last_name, 1))
            else:
                await db.execute('''
                                            INSERT INTO users (user_id, firstname, lastname) VALUES (?, ?, ?)
                                            ''',
                                 (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await db.commit()


async def count_users():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT COUNT(*) FROM users')
        result = await cursor.fetchone()
        return result[0]


async def count_subscriptions():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT COUNT(*) FROM apscheduler_jobs')
        result = await cursor.fetchone()
        return result[0]


async def get_user(user_id: int):
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return await cursor.fetchone()


async def get_users():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT * FROM users')
        return await cursor.fetchall()


async def set_status_active_user(user_id: int, status: int):
    async with aiosqlite.connect(settings.db.db_name) as db:
        await db.execute('UPDATE users SET is_active = ? WHERE user_id = ?', (status, user_id,))
        await db.commit()


async def count_active_users():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT COUNT(*) FROM users  WHERE is_active = 1')
        result = await cursor.fetchone()
        return result[0]


async def increase_counter_received_messages(user_id: int):
    async with aiosqlite.connect(settings.db.db_name) as db:
        await db.execute('update users set msg_recieved = msg_recieved + 1 where user_id = ?', (user_id,))
        await db.commit()


async def total_received_messages():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('select sum(msg_recieved) from users')
        result = await cursor.fetchone()
        return result[0]


async def get_last_registered_user():
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('select * from users order by id desc limit 1')
        return await cursor.fetchone()


async def is_privileged_user(user_id: int):
    async with aiosqlite.connect(settings.db.db_name) as db:
        cursor: Cursor = await db.execute('SELECT is_privileged FROM users WHERE user_id = ?', (user_id,))
        result = await cursor.fetchone()
        return bool(result[0])
