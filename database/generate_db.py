import asyncio

from database.async_db import AsyncDatabase

db = AsyncDatabase()

asyncio.run(db.generate_data())