import asyncio

from async_db import AsyncDatabase

db = AsyncDatabase()

asyncio.run(db.generate_data())