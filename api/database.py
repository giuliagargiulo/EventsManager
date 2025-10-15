import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL", "got nothing")

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def get_db():
    db = await get_connection()
    try:
        yield db
    finally:
        await db.close()
