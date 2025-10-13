import asyncpg
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = "postgresql://postgres:postgres@db:5432/giuliagargiulo"

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def get_db():
    db = await get_connection()
    try:
        yield db
    finally:
        await db.close()