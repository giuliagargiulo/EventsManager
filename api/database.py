import os
import databases

DATABASE_URL = os.getenv("DATABASE_URL", "got nothing")

database = databases.Database(DATABASE_URL)

async def get_db():
    if not database.is_connected:
        await database.connect()
    try:
        yield database
    finally:
        if database.is_connected:
            await database.disconnect()
            
