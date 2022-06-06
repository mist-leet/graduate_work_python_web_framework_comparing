import asyncio

from async_db import AsyncDatabase, SyncDatabase

db = SyncDatabase()

db.get_data_by_like()

# asyncio.run(db.generate_data())